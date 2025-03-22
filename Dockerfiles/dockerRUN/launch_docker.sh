xhost +
docker run -it --rm -v /scratch/code/tesi_code/src/myTesiCode:/root/ff_ws/src/myTesiCode -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=$DISPLAY --network host --name serverNavRos rmf_all_imagev1.1  bash

docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=$DISPLAY --network host --name serverNavRos rmf_all_imagev1.1  bash
