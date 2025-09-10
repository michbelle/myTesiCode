import rclpy
from rclpy.node import Node
from nav2_msgs.srv import ComputePathToPose
from geometry_msgs.msg import PoseStamped

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')
        self.client = self.create_client(ComputePathToPose, 'compute_path_to_pose')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for ComputePathToPose service...')
        
        self.initial_pose = PoseStamped()
        self.goal_pose = PoseStamped()

        # Set initial position
        self.initial_pose.header.frame_id = 'map'
        self.initial_pose.pose.position.x = 1.0
        self.initial_pose.pose.position.y = 1.0
        self.initial_pose.pose.orientation.w = 1.0

        # Set goal position
        self.goal_pose.header.frame_id = 'map'
        self.goal_pose.pose.position.x = 5.0
        self.goal_pose.pose.position.y = 5.0
        self.goal_pose.pose.orientation.w = 1.0

        self.compute_path()

    def compute_path(self):
        request = ComputePathToPose.Request()
        request.start = self.initial_pose
        request.goal = self.goal_pose

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info('Path computed successfully!')
            path = future.result().path
            self.get_logger().info(f'Path: {path}')
        else:
            self.get_logger().error('Failed to compute path.')

def main(args=None):
    rclpy.init(args=args)
    path_planner_node = PathPlannerNode()
    rclpy.spin(path_planner_node)
    path_planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()