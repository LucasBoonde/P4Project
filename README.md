# P4Project
This is the repository for the P4 project about autonomous parallel asphalt crack sealing robot.

HOW TO NAVIGATE IN THE GITHUB:

FOLDERS:
- 5_bar_parallelrobot: 
This folder includes all calculations for kinematic- and dynamic equations. The TrajectoryPlanningCBPOLY.m calculates the trajectories for the motor angles, angular velocities and accelerations. 

- Dynamixel_mega:
Arduino script to communicate to the dynamixel motors.

- Mid_way_connection:
Arduino script recives a message from computer and sends it to dynamixel arduino board.

- SolidWorks:
SolidWorks files for all design considerations described in this project. This also includes STL files for 3D printed parts, if useful for other students. These lay under "STL-Files"

- VideosOfTests:
Video of the bitumen test. Video of the movement of the robot, and a video showing the entire setup.

HOW TO USE THE GITHUB TO CONTROL THE ROBOT:
1. First (x,y) points are put into the Forward_Invers_Kinematik_5_bar.m in the inverse section, to calculate the theta angles for the two motors.

2. Run the main.py and see the theta angles given in radians.

3. In a new tab, open TrajectoryPlanningCBPOLY.m, and place first the angles from main.py, and then from Forward_Invers_Kinematik_5_bar.m in points1 and points2. Chose time-stepts (ts) and velocities1 and 2. 

4. Run the script to generate the trajectories for the given points.

5. restart the main.py script to include the new calculations, type "Go" in the console, and let the robot move between the points. 

