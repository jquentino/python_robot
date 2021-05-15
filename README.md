# Python Robot

## My motivation
This is a classical problem project in some introductory robotic programming courses, despite I didn't do such courses I decided to wrote this solution to improve my object-oriented skills in Python.

## Project description
The code simulates a robot navigating in an environment with many obstacles. The environment is represented by a grid, and the robot has as objective to reach a target coordinate of this grid. 

The inputs are the initial and target coordinates, the dimensions of the environment grid and the obstacles coordinates. The output is an animation of the steps that the robot does to reach its objective. 

To detect the obstacles, the robot uses a laser sensor, which has a limited range of detection, the parameter that sets this range can be changed too. For calculating the best trajectory I make the robot computes a potential field based on what obstacles he knows, and then he tries to move in direction of the lowest potential. 

The next figure represents how the potential field works:

![image](https://user-images.githubusercontent.com/61889205/118342472-ecf0ea00-b4f9-11eb-8ede-fcd8b363f851.png)

Some comments in the code aren't in English, I pretend to correct this and make some improvements in the 'project.py' later.
