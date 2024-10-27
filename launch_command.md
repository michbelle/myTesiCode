ros2 launch myCode 0_mini_gazebo.launch.py

ros2 launch myCode 1_robot_localizer.launch.py

ros2 launch myCode 2_navigation_launch.py

ros2 launch myCode 3_slam_launch.py

export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

map:=/home/michele/tesi_code/src/myCode/maps/my_map.yaml


## docker

docker run -it --net=host --privileged --env="DISPLAY=$DISPLAY" --volume="${XAUTHORITY}:/root/.Xauthority" --volume="/home/michele/tesi_code:/tesi_code" osrf/ros:humble-desktop-full

docker start affectionate_sinoussi

docker exec -it affectionate_sinoussi /bin/bash

#### vim
source /tesi_code/install/setup.bash
source /opt/ros/humble/setup.bash