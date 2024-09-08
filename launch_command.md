ros2 launch myCode 0_mini_gazebo.launch.py

ros2 launch myCode 1_robot_localizer.launch.py

ros2 launch myCode 2_navigation_launch.py

ros2 launch myCode 3_slam_launch.py

export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

map:=/home/michele/tesi_code/src/myCode/maps/my_map.yaml