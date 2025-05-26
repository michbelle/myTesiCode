import rclpy
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node

class NavigateToPoseClient(Node):
    def __init__(self):
        super().__init__('navigate_to_pose_client')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, goal_pose):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose
        self._action_client.wait_for_server()
        self.send_goal_future = self._action_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted, waiting for result...')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: %s' % result)

def main(args=None):
    rclpy.init(args=args)
    client = NavigateToPoseClient()
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = client.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0
    client.send_goal(goal_pose)
    rclpy.spin(client)
    client.destroy_node()
    rclpy.shutdown()

import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class PathPlanner(Node):

    def __init__(self):
        super().__init__('path_planner')
        self.navigator = BasicNavigator()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def plan_path(self, goal_pose):
        # Wait for the Nav2 stack to be fully operational
        self.navigator.waitUntilNav2Active()

        # Set the goal pose
        goal_pose_msg = PoseStamped()
        goal_pose_msg.header.frame_id = 'map'
        goal_pose_msg.pose.position.x = goal_pose['x']
        goal_pose_msg.pose.position.y = goal_pose['y']
        goal_pose_msg.pose.orientation.z = goal_pose['z']
        goal_pose_msg.pose.orientation.w = goal_pose['w']

        # Plan the path
        self.navigator.goToPose(goal_pose_msg)

        # Wait for the path to be planned
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                print(f"Feedback: {feedback}")
            rclpy.spin_once(self, timeout_sec=0.1)

        # Get the planned path
        planned_path = self.navigator.getPath()
        if planned_path:
            print("Planned path:")
            for pose in planned_path.poses:
                print(f"Pose: x={pose.pose.position.x}, y={pose.pose.position.y}, z={pose.pose.orientation.z}, w={pose.pose.orientation.w}")
        else:
            print("No path planned.")

        # Cancel the task to avoid moving the robot
        self.navigator.cancelTask()

def main(args=None):
    rclpy.init(args=args)
    path_planner = PathPlanner()

    # Define the goal pose
    goal_pose = {
        'x': 1.0,
        'y': 2.0,
        'z': 0.0,
        'w': 1.0
    }

    # Plan the path
    path_planner.plan_path(goal_pose)

    rclpy.shutdown()



if __name__ == '__main__':
    main()
