RMF_SERVER_URL=http://localhost:8000
TRAJECTORY_SERVER_URL=ws://localhost:8006

docker run   --network host -it --rm   -e ROS_DOMAIN_ID=0   -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp   ghcr.io/open-rmf/rmf-web/api-server:latest