import rospy
import time
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

# Initialize the ROS node
rospy.init_node('path_planner_timer')

# Create an action client for the move_base action
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

# Create a goal
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()
goal.target_pose.pose.position.x = 1.0
goal.target_pose.pose.position.y = 1.0
goal.target_pose.pose.orientation.w = 1.0

# Start timing
start_time = time.time()

# Send the goal to the action server
client.send_goal(goal)
client.wait_for_result()

# End timing
end_time = time.time()

# Calculate the duration
duration = end_time - start_time
rospy.loginfo("Time taken to generate path: {:.2f} seconds".format(duration))
