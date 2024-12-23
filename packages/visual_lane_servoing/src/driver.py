import sys
import subprocess
# Function to install packages
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
import base64
from PIL import Image
import io
import os
import cv2

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("Write your key here")



# Function to encode image to Base64
def encode_image_to_base64(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.resize((64, 64), Image.ANTIALIAS)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Error encoding image: {e}")


# Function to send messages to GPT-4 Turbo
def send_to_gpt(messages):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            response_format={"type": "text"},
            temperature=0.1,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with GPT: {e}"


# Driving Simulation Function for ROS Node
def driving_simulation_response(image_path):
    # Initial examples (replace with real example paths)
    # images_name = [
    #     "example1.png",
    #     "example2.png",
    #     "example3.png"
    # ]
    #
    # images = [
    #     encode_image_to_base64(images_name[0]),
    #     encode_image_to_base64(images_name[1]),
    #     encode_image_to_base64(images_name[2]),
    # ]

    # Build initial conversation
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Follow this instruction for any photos that I give to you and provide me with the output\n\n"
                        "<General instruction block>\n"
                        "You are an expert driver of the car.\n"
                        "Your job is to give a velocity and direction pattern based on the input for now, 0.5 seconds later, "
                        "and 1 second later from the current time.\n"
                        "Your goal is to safely drive without damaging any ducks which are civilians in our town and explore the city. \n"
                        "The input is an image 64 * 64 from the driver's point of view. You have to decide the action based on the "
                        "current position of the car. The bottom of the image is the closest part to the car.\n"
                        "The street is divided into two ways by yellow dashed lines. The road boundary is marked by white lines on both sides of the road.\n"
                        "You will always give the output in the correct format no matter what the input is.\n\n"
                        "<Output format definition block>\n"
                        "The following are rules for describing the velocity and direction pattern:\n"
                        "1. You should first output the velocity, then the direction for the current time, then the velocity for 0.2 sec later and "
                        "the direction for that time, and then the velocity for 0.4 sec and the direction for that.\n"
                        "2. There are two velocities to choose from: [0.0, 0.2].\n"
                        "3. A direction could be written as LL, L, F, R, RR, and S for 45 degrees to left, 20 degrees to left, forward, "
                        "20 degrees to right, 45 degrees to right, and stop.\n\n"
                        "<Examples block>\nInput:"
                    ),
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://i.ibb.co/JH2XQxG/example1.png" #f"data:image/png;base64,{images[0]}"
                  }
                },
                {
                  "type": "text",
                  "text": "Output:\n0.2 F\n0.2 L\n0.2 L\nInput:"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://i.ibb.co/sWzDFsp/example2.png" #f"data:image/png;base64,{images[1]}"
                  }
                },
                {
                  "type": "text",
                  "text": "Output:\n0.2 F\n0.2 F\n0.2 F\nInput:"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://i.ibb.co/0c9Ysxp/example3.png" #f"data:image/png;base64,{images[2]}"
                  }
                },
                {
                  "type": "text",
                  "text": "Output:\n0.2 RR\n0.2 R\n0.2 R"
                }
            ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Please provide the image you want analyzed for the driving simulation instructions."
            }
          ]
        },
    ]

    # Encode the new image to Base64
    # try:
    #     image_base64 = encode_image_to_base64(image_path)
    # except ValueError as e:
    #     return str(e)
    image_base64 = image_path
    # Add the user's image and input to the conversation
    messages.extend([
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
        ]}
    ])

    # Send messages to GPT
    gpt_response = send_to_gpt(messages)

    # Return the response
    return gpt_response