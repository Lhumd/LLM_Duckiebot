<p align="center">
<img src="./assets/images/dtlogo.png" alt="Duckietown Logo" width="50%">
</p>

# LLM Duckiebot

## Introduction
The integration of Large Language Models (LLMs) into robotics has opened up new avenues for intelligent control systems. This project explores how LLMs can drive a Duckiebot autonomously using visual inputs and structured patterns, as well as manage quadrupedal locomotion via natural language commands. By combining robotics with the power of LLMs, we aim to bridge the gap between machine intelligence and real-world applications.

## Motivation
Robotics relies heavily on precise and predefined control algorithms. However, traditional approaches struggle with adaptability and dynamic tasks. LLMs, with their capability to process and respond to natural language, present an opportunity to simplify and generalize robotic control. This project investigates:

* Whether LLMs can effectively interpret input (e.g., images, commands) for robotic control.
* The challenges of integrating LLMs into real-time robotic applications, such as autonomous driving and quadrupedal movement.

## Method
### Quadrupedal Locomotion (Previous work)
Using the [SayTap](https://saytap.github.io/) Method, natural language commands are translated into movement sequences for quadrupedal robots. The framework leverages a limited number of demonstrations to train and guide the robot’s actions.
### Duckiebot Driving
Duckiebot navigates based on visual inputs (64x64 pixel images) and outputs a structured sequence of velocities and directions over time. Key rules include:

1. Velocities: [0.0, 0.2].
2. Directions: [LL, L, F, R, RR, S].

Example output: 0.2 F 0.2 F 0.2 RR
Input instruction:
   
      Follow this instruction for any photos that I give to you and provide me with the output
      <General instruction block>
      You are an expert driver of the car. Your job is to give a velocity and direction pattern based on the input for now, 0.2 seconds later, and 0.4 second later from the current time.Your goal is to safely drive without damaging any ducks which are civilians in our town and explore the city. The input is an image 64 * 64 from the driver's point of view. You have to decide the action based on the current position of the car. The bottom of the image is the closest part to the car.The street is divided into two ways by yellow dashed lines. The road boundary is marked by white lines on both sides of the road. You will always give the output in the correct format no matter what the input is.
      
      <Output format definition block>
      The following are rules for describing the velocity and direction pattern:
      1. You should first output the velocity, then the direction for the current time, then the velocity for 0.2 sec later and the direction for that time, and then the velocity for 0.4 sec and the direction for that.
      2. There are two velocities to choose from: [0.0, 0.2].
      3. A direction could be written as LL, L, F, R, RR, and S for 45 degrees to left, 20 degrees to left, forward, 20 degrees to right, 45 degrees to right, and stop.
      
      <Examples block>
      Input:
      
      	    Output: 
                0.2 F							0.2 F							0.2 RR
      	    0.2 L							0.2 F							0.2 R
      	    0.2 L							0.2 F							0.2 R
                   
      	  


## Results
### Observations
1. Quadrupedal Locomotion:
* Performance deteriorates with an increasing number of demonstrations, indicating that fewer, high-quality examples yield better results.
* Reference: SayTap: Language to Quadrupedal Locomotion.
2. Duckiebot Driving:
* LLMs exhibit a strong dependency on patterns and predefined examples.
* Continuous tasks require resetting instructions, highlighting a limitation in maintaining task context.
## Challenges
* High dependence on training patterns rather than logical reasoning.
* Inefficient handling of continuous commands without resetting instructions.

For a detailed deep-dive, see our [Presentation](https://docs.google.com/presentation/d/1iGbgDfPQP9gEIzcXKrSCXH6V1ELKVtwjplxxmRdpl0U/edit#slide=id.g31c0eb301aa_0_55).

# Instructions

**NOTE:** All commands below are intended to be executed from the root directory of this repo (i.e., the directory containing this `README`).


## 1. Make sure your repo is up-to-date

Update your repo definition and instructions,

    git pull upstream ente

**NOTE:** to pull from upstream, you need to have completed the instructions in the [duckietown-lx repository README](https://github.com/duckietown/duckietown-lx/blob/mooc2022/README.md) to *fork* this repository.


## 2. Make sure your system is up-to-date

- 💻 Always make sure your Duckietown Shell is updated to the latest version. See [installation instructions](https://github.com/duckietown/duckietown-shell)

This repo is meant to be run with the `ente` version of the shell commands. You can switch to that version with `dts profile switch ente`. 

- 💻 Update the shell commands: `dts update`

- 💻 Update your laptop/desktop: `dts desktop update`

- 🚙 Update your Duckiebot: `dts duckiebot update ROBOTNAME` (where `ROBOTNAME` is the name of your (real or virtual - more on this later) Duckiebot chosen during the initialization procedure.)

## 3. Configure OpenAI API Key
This repository uses OpenAI APIs for generating actions based on input. Ensure that you:

1. Obtain an OpenAI API key from OpenAI.
2. Update the api_key variable in the file visual_lane_servoing_node with your OpenAI API key.

## 4. Work on the repo


### Launch the code editor

Open the code editor by running the following command,

```
dts code editor
```

Wait for a URL to appear on the terminal, then click on it or copy-paste it in the address bar
of your browser to access the code editor. The first thing you will see in the code editor is
this same document, you can continue there.


### Walkthrough of notebooks

**NOTE**: You should be reading this from inside the code editor in your browser.

Inside the code editor, use the navigator sidebar on the left-hand side to navigate to the
`notebooks` directory and open the first notebook.

Follow the instructions on the notebook and work through the notebooks in sequence.


### Building your code

You can build your code with 

```
dts code build -R ROBOT_NAME
```

This will build a docker image with your code compiled inside - you should your ROS node get built during the process. 


### Testing with Duckiematrix

In order to test your code in the Duckiematrix you will need a virtual robot. You can create one with the command:

```
dts duckiebot virtual create [VIRTUAL_ROBOT_NAME]
```

where `[VIRTUAL_ROBOT_NAME]` can be anything you like (but remember it for later).

Then you can start your virtual robot with the command:

```
dts duckiebot virtual start [VIRTUAL_ROBOT_NAME]
```

You should see it with a status `Booting` and finally `Ready` if you look at `dts fleet discover`: 

```
     | Hardware |   Type    | Model |  Status  | Hostname 
---  | -------- | --------- | ----- | -------- | ---------
vbot |  virtual | duckiebot | DB21J |  Ready   | vbot.local
```

Now that your virtual robot is ready you can start the Duckiematrix. From this exercise directory do:

```
dts code start_matrix
```

You should see the Unity-based Duckiematrix simulator start up. 


### 💻 Testing 


To test your code in the duckiematrix you can do:

```
dts code workbench -m -R [VIRTUAL_ROBOT_NAME]
```

and to test your code on your real Duckiebot you can do:

```
dts code workbench -R [ROBOT_NAME]
```


In another terminal, you can launch the `noVNC` viewer for this exercise which can be useful to send commands to the robot and view the odometry that you calculating in the RViZ window. 

```
dts code vnc -R [ROBOT_NAME]
```

where `[ROBOT_NAME]` could be the real or the virtual robot (use whichever you ran the `dts code workbench` and `dts code build` command with).

In the noVNC desktop, click on the icon marked "VLS - Visual Lane Servoing repo" and then you should follw the prompts
in the terminal where you ran `dts code workbench`.
