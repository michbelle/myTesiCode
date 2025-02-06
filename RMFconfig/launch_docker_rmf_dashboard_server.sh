RMF_SERVER_URL=http://localhost:8000
TRAJECTORY_SERVER_URL=ws://localhost:8006

docker run   --network host -it --rm   -e RMF_SERVER_URL=$RMF_SERVER_URL   -e TRAJECTORY_SERVER_URL=$TRAJECTORY_SERVER_URL   ghcr.io/open-rmf/rmf-web/demo-dashboard:latest