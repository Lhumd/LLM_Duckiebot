<p align="center">
<img src="./assets/images/dtlogo.png" alt="Duckietown Logo" width="50%">
</p>

# LLM Duckiebot
This repository explores the integration of Large Language Models (LLMs) with robotics, specifically focusing on Duckiebot for autonomous driving using image-based input and structured patterns. Additionally, the repository highlights experiments in quadrupedal locomotion using language commands.

Case Study: Language to Quadrupedal Locomotion and Duckiebot Driving
## Overview
This case study demonstrates the challenges and methodologies of using LLMs for robotic control. The focus areas include:

1. <b> Quadrupedal Locomotion: </b> Translating natural language commands into actionable movement patterns.
2. <b> Duckiebot Driving: </b>  Using a Duckiebot to navigate based on visual input and predefined driving rules.
   
## Methodology
<b>Language to Quadrupedal Locomotion </b> 

Using the SayTap Method, quadrupedal robots respond to natural language commands with predefined motion sequences.

<b>Language to Duckiebot Driving </b> 

Duckiebot interprets 64x64 pixel images to decide velocity and direction patterns. Outputs are structured as sequences (e.g., 0.2 F 0.2 F 0.2 RR).

## Observations and Challenges
<b>Quadrupedal Locomotion: </b>

    - Performance degrades with more training examples.
<b>Duckiebot Driving: </b>

    - LLMs heavily rely on patterns and struggle without detailed examples.
    - Continuous commands require resetting instructions.
## Future Work

For a detailed deep-dive, see our [Presentation]([https://github.com/duckietown/duckietown-shell](https://docs.google.com/presentation/d/1iGbgDfPQP9gEIzcXKrSCXH6V1ELKVtwjplxxmRdpl0U/edit#slide=id.g31c0eb301aa_0_55)).

# Instructions

**NOTE:** All commands below are intended to be executed from the root directory of this exercise (i.e., the directory containing this `README`).


## 1. Make sure your exercise is up-to-date

Update your exercise definition and instructions,

    git pull upstream ente

**NOTE:** to pull from upstream, you need to have completed the instructions in the [duckietown-lx repository README](https://github.com/duckietown/duckietown-lx/blob/mooc2022/README.md) to *fork* this repository.


## 2. Make sure your system is up-to-date

- 💻 Always make sure your Duckietown Shell is updated to the latest version. See [installation instructions](https://github.com/duckietown/duckietown-shell)

This exercise is meant to be run with the `ente` version of the shell commands. You can switch to that version with `dts profile switch ente`. 

- 💻 Update the shell commands: `dts update`

- 💻 Update your laptop/desktop: `dts desktop update`

- 🚙 Update your Duckiebot: `dts duckiebot update ROBOTNAME` (where `ROBOTNAME` is the name of your (real or virtual - more on this later) Duckiebot chosen during the initialization procedure.)

## 3. Configure OpenAI API Key
This repository uses OpenAI APIs for generating actions based on input. Ensure that you:

1. Obtain an OpenAI API key from OpenAI.
2. Update the api_key variable in the file visual_lane_servoing_node with your OpenAI API key.

## 4. Work on the exercise


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

In the noVNC desktop, click on the icon marked "VLS - Visual Lane Servoing Exercise" and then you should follw the prompts
in the terminal where you ran `dts code workbench`.

Now you can proceed to the [first notebook](./notebooks/01-Pinhole-Camera/pinhole_camera_matrix.ipynb).

