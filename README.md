# Implementation of Tic Tac Toe in Augmented Reality using OpenCV in Python

## Description
This project is an implementation of the classic game Tic Tac Toe in a augmented reality (AR) environment using OpenCV library in Python. It allows players to play the game by drawing wich is captured by a webcam. The opponents turn will be displayed at the screen, creating an interactive game experience. 

This is the final project of the Introduction to Image Processing course. The project involved implementing the "Augmented Reality Tic-Tac-Toe" article by Joe Maguire and David Saltzman from Stanford University. The technical aspects of the implementation focused on utilizing the OpenCV library to create a Python-based Tic-Tac-Toe game. The implementation incorporated concepts such as homography and image features, with the SIFT algorithm being used for feature detection.

# How it Works 
The code was divided into two files: one for computer vision tasks and the other for the game logic, which served as a library for the main program. The computer vision part involved using a reference image and projecting the corresponding symbols onto the game board using the obtained homography matrix. The RANSAC algorithm from the OpenCV library was used for point selection. 

The game logic followed a sequence of prioritized strategies to ensure optimal moves and prevent the opponent from winning. The AI player attempted to win the game first, followed by blocking the opponent's winning moves, and then occupied the center position if available. If none of these conditions were met, the AI made strategic moves based on the positions of existing symbols on the board. The implementation used a template matching technique with a rotated template to identify the "X" symbol in the camera feed. The report provides an overview of the implementation process, emphasizing the application of learned concepts and techniques from the Introduction to Image Processing course.

# How to use it
Run the "main.py" file and do the following steps:
- Draw the Tic-Tac-Toe game board.
- Align the board centrally with the camera and press the "P" key for the program to detect image features.
- Position it in the desired position so that the camera captures the entire board.
- Draw an "X" in the desired position and wait for the AI's response.
- Repeat the previous step until the end of the game.
- Press the "R" key to restart.

# Links
Demo: https://youtu.be/OyUPyRpV3JU
Reository: https://github.com/CristovaoBG/VR-tic-tac-toe
Original project: https://stacks.stanford.edu/file/druid:np318ty6250/Maguire_Saltzman_Augmented_Reality_Tic_Tac_Toe.pdf

# Author
Cristóvão B. Gomes
cristovao@live.com