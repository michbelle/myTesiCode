#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped


from rclpy.action import ActionClient

from nav2_msgs.action import ComputePathToPose

class ClickedPointListener(Node):

    def __init__(self):
        super().__init__('clicked_point_listener')
        self.subscription = self.create_subscription(
            PointStamped,
            '/clicked_point',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning


        self._action_client = ActionClient(self, ComputePathToPose, '/compute_path_to_pose')

    def listener_callback(self, msg):
        # Extract x and y values from the PointStamped message
        x = msg.point.x
        y = msg.point.y
        self.get_logger().info(f'Received point: x={x}, y={y}')
        self.calculate_path_to(x,y)
    
    def calculate_path_to(self, x, y):
        goal_msg = ComputePathToPose.Goal()
        goal_msg.goal.header.frame_id = 'map'
        goal_msg.goal.pose.position.x = x
        goal_msg.goal.pose.position.y = y
        goal_msg.goal.pose.position.z = 0.0
        goal_msg.goal.pose.orientation.x = 0.0
        goal_msg.goal.pose.orientation.y = 0.0
        goal_msg.goal.pose.orientation.z = 0.0
        goal_msg.goal.pose.orientation.w = 1.0

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if hasattr(result, 'error_code'):
            if result.error_code != 0:
                self.get_logger().error('Result: {0}'.format(result))
        else:
            try:
                self.get_logger().info(f'Obtained path in {result.planning_time.sec},{result.planning_time.nanosec}')
            except Exception as e:
                print(e)

        self.get_logger().debug('---------------------------')
        self.get_logger().debug('Result: {0}'.format(result))
        self.get_logger().debug('---------------------------')
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback))

def main(args=None):
    rclpy.init(args=args)
    clicked_point_listener = ClickedPointListener()
    rclpy.spin(clicked_point_listener)
    clicked_point_listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
