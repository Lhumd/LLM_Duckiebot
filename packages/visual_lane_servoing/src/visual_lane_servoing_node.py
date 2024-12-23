#!/usr/bin/env python3

import os
import cv2
import yaml
import time
import rospy
import numpy as np

from duckietown_msgs.msg import Twist2DStamped, EpisodeStart
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

from visual_lane_servoing.include import visual_servoing_solution
from duckietown.dtros import DTROS, NodeType, TopicType
from duckietown.utils.image.ros import compressed_imgmsg_to_rgb, rgb_to_compressed_imgmsg
from PIL import Image
import base64
import io
from driver import driving_simulation_response




class LaneServoingNode(DTROS):
    """
    Performs a form of visual servoing based on estimates of the image-space lane orientation
    Args:
        node_name (:obj:`str`): a unique, descriptive name for the ROS node
    Configuration:

    Publisher:
        ~wheels_cmd (:obj:`WheelsCmdStamped`): The corresponding resulting wheel commands
    Subscribers:
        ~/image/compressed (:obj:`CompressedImage`):
            compressed image
    """

    def __init__(self, node_name):
        # Initialize the DTROS parent class
        super(LaneServoingNode, self).__init__(node_name=node_name, node_type=NodeType.LOCALIZATION)
        self.loginfo("Initializing...")
        # get the name of the robot
        self.veh = rospy.get_namespace().strip("/")
        self.v_0 = 0.083  # Default forward velocity
        self.omega_max = 1.0  # Default maximum angular velocity
        self.VLS_ACTION = None
        self.VLS_STOPPED = True

        # Defining subscribers:
        rospy.Subscriber(
            f"/{self.veh}/rectifier_node/image/compressed",
            CompressedImage,
            self.cb_image,
            buff_size=10000000,
            queue_size=1,
        )

        # select the current activity
        rospy.Subscriber(f"/{self.veh}/vls_node/action", String, self.cb_action, queue_size=1)

        # Command publisher
        car_cmd_topic = f"/{self.veh}/joy_mapper_node/car_cmd"
        self.pub_car_cmd = rospy.Publisher(
            car_cmd_topic, Twist2DStamped, queue_size=1, dt_topic_type=TopicType.CONTROL
        )

        self.loginfo("Initialized!")

    def cb_action(self, msg):
        """
        Call the right functions according to desktop icon the parameter.
        """
        self.VLS_ACTION = msg.data
        self.loginfo(f"ACTION: {self.VLS_ACTION}")

        if self.VLS_ACTION == "stop":
            self.publish_command([0, 0])
            self.VLS_STOPPED = True
            return
        elif self.VLS_ACTION == "go":
            self.VLS_STOPPED = False
            # NOTE: this is needed to trigger the agent and get another image back
            self.publish_command([0, 0])
            return

    def cb_image(self, image_msg):
        """
        Processes the incoming image messages.

        Performs the following steps for each incoming image:

        #. Resizes the image to the ``~img_size`` resolution
        #. Removes some amount of the image

        Args:
            image_msg (:obj:`sensor_msgs.msg.CompressedImage`): The received image message

        """

        self.loginfo("Processing image for GPT-4-based driving simulation...")
        # Convert ROS CompressedImage to OpenCV image
        image = compressed_imgmsg_to_rgb(image_msg)

        # Convert OpenCV image to Base64
        image_base64 = self.image_to_base64(image)

        # Get GPT-4 response
        gpt_response = driving_simulation_response(image_base64)
        self.loginfo(f"GPT Response: {gpt_response}")

        # Parse GPT response and generate robot commands
        velocity, omega = self.parse_gpt_response(gpt_response)
        u = [(velocity * 5) * self.v_0 * 5, omega]
        # print("U", u)
        self.publish_command(u)

    def image_to_base64(self, image):
        try:
            # Convert OpenCV image to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            self.logerr(f"Error converting image to Base64: {e}")
            return None

    def parse_gpt_response(self, response):
        try:
            print("response:", response)
            print("_____________________")
            # Example parsing logic (adjust based on GPT-4 output format)
            lines = response.split("\n")
            direction = "S"
            velocity = 0.0
            for line in lines:
                # Skip empty lines and lines without enough data
                if not line.strip() or len(line.split()) < 2:
                    continue

                # Try to parse the line as velocity and direction
                try:
                    velocity = float(line.split()[0])  # First element: velocity
                    direction = line.split()[1]  # Second element: direction
                    break  # Exit the loop after successfully parsing
                except ValueError:
                    # If parsing fails, continue to the next line
                    continue


            # Map direction to angular velocity
            omega_mapping = {
                "LL": -0.5 * self.omega_max,
                "L": -0.2 * self.omega_max,
                "F": 0.0,
                "R": 0.2 * self.omega_max,
                "RR": 0.5 * self.omega_max,
                "S": 0.0,
            }
            print("direction", direction)
            omega = omega_mapping.get(direction, 0.0)
            return velocity, omega
        except Exception as e:
            self.logerr(f"Error parsing GPT response: {e}")
            return 0.0, 0.0

    def publish_command(self, u):
        """Publishes a car command message.

        Args:
            u (:obj:`tuple(double, double)`): tuple containing [v, w] for the control action.
        """

        car_control_msg = Twist2DStamped()
        car_control_msg.header.stamp = rospy.Time.now()

        car_control_msg.v = u[0]  # v
        car_control_msg.omega = u[1]  # omega

        self.pub_car_cmd.publish(car_control_msg)

    def on_shutdown(self):
        self.loginfo("Stopping motors...")
        self.publish_command([0, 0])
        time.sleep(0.5)
        self.loginfo("Motors stopped.")

if __name__ == "__main__":
    import sys
    import subprocess
    def install(package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")
            sys.exit(1)


    # Ensure the 'openai' package is installed

    install("pandas")
    print("~~~~~~~pandas~~~~~~~")
    install("openai")
    print("~~~~~~~openai~~~~~~~")
    install("flask")
    print("~~~~~~~flask~~~~~~~")
    from flask import Flask, request, jsonify, render_template
    import openai

    # Initialize Flask app
    app = Flask(__name__)

    # Set your OpenAI API key
    api_key = "Write your key here"
    openai.api_key = os.getenv(api_key)

    os.environ["OPENAI_API_KEY"] = api_key
    # Write the API key to a file
    shell_config = os.path.expanduser("~/.bashrc")  # Or "~/.zshrc" for Zsh users
    export_command = f'export OPENAI_API_KEY="{api_key}"\n'

    with open(shell_config, "a") as file:
        file.write(export_command)

    # Initialize the node
    encoder_pose_node = LaneServoingNode(node_name="visual_lane_servoing_node")
    # Keep it spinning
    rospy.spin()
