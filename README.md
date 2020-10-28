# Gesture-Based-Drone-Controller
Simulating a drone controller using head pose estimation and facial landmark detection.

## Simulator In Action

![Simulator In Action](Media/SimulatorDemo.gif)

## Python Packages Required
* cv2
* dlib
* numpy
* pynput

## Steps
1. Open *Assets/RealSimulEnv* scene in Unity, and click on Run to start the simulator.
2. Use the following command to run the python based controller script (make sure that you are in ./Python Scripts/ directory):
> python PoseEstimatorAndController.py
3. Focus back on the Game Tab in Unity. Move your head to control the roll, pitch and yaw of the drone in accordance to the given diagrams. Open mouth for upward thrust.





