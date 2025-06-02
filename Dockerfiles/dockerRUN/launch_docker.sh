
xhost local:root

path_repo=/scratch/code/

docker run -it --rm \
    -v $path_repo/tesi_code/src/myTesiCode:/root/ff_ws/src/myTesiCode \
    -v $path_repo/tesi_code/src/DStar-Trajectory-Planner:/root/ff_ws/src/DStar-Trajectory-Planner \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro --device=/dev/dri:/dev/dri -e DISPLAY=$DISPLAY \
    --network host \
    --name serverNavRos \
    rmf_all_imagev1.1  \
    bash -c "cd /root/ff_ws && colcon build --symlink-install --packages-select myCode && bash"