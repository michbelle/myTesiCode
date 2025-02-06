# Server RMF with simulation

# add AS builder to have a build enviroment see internet about
ARG rosimage=osrf/ros:jazzy-desktop-full
ARG extworkdir=/scratch/code/tesi_code

FROM $rosimage

#install Core rmf
RUN mkdir -p ~/ff_ws/src \
    && apt update && apt install ros-dev-tools -y && apt install -y ros-jazzy-rmf-dev \
    && apt update && apt install -y wget python3-pip python3-vcstool ros-jazzy-rmw-cyclonedds-cpp \
    && pip3 install eclipse-zenoh==1.1.0 pycdr2 rosbags --break-system-packages \
    && source /opt/ros/jazzy/setup.bash \
    && wget https://raw.githubusercontent.com/open-rmf/rmf/main/rmf.repos \
    && vcs import ~/ff_ws/src < rmf.repos
RUN cd ~/ff_ws/src \
    && source /opt/ros/jazzy/setup.bash \
    && git clone https://github.com/open-rmf/free_fleet \
    && cd ~/ff_ws \
    && rosdep install --from-paths src --ignore-src --rosdistro jazzy -yr \
    && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release

#install simulation code
RUN apt update && apt install -y ros-jazzy-nav2-bringup git \
    && git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations ~/turtlebot3_simulations \
    && printf "source /opt/ros/jazzy/setup.bash\nexport RMW_IMPLEMENTATION=rmw_cyclonedds_cpp\nexport GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/turtlebot3_simulations/turtlebot3_gazebo/models" >> ~/.bashrc \
    && rm -rf /var/lib/apt/lists/*

#install zenoh
RUN echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null \
    && apt update \
    && apt install -y systemctl \
    && apt install -y zenoh

#copy my code
COPY $extworkdir /code/

#set simulation robot for nav2
ENV TURTLEBOT3_MODEL=burger

#FROM osrf/ros:humble-desktop-full AS builder