xhost +local:docker
docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=$DISPLAY --name server_rmf --privileged --network host rmf:latest bash