ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "pose: {header: {frame_id: map}, pose: {position: {x: 6.0, y: 22.0, z: 0.0}, orientation:{x: 0.0, y: 0.0, z: 0, w: 1.0000000}}}


ros2 topic echo /clicked_point #to subscribe the topic generated publishing data from rviz
ros2 action send_goal /compute_path_to_pose nav2_msgs/action/ComputePathToPose "goal: {header: {frame_id: map}, pose: {position: {x: 14.844, y: 58.48, z: 0.0}, orientation:{x: 0.0, y: 0.0, z: 0, w: 1.0000000}}}"