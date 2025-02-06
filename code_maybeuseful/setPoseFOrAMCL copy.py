import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.srv import SetInitialPose

#TOtest
#
#or
#ros2 topic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped '{ header: {stamp: {sec: 0, nanosec: 0}, frame_id: "map"}, pose: { pose: {position: {x: 0.1, y: 0.0, z: 0.0}, orientation: {w: 0.1}}, } }'

# or cheat
# https://youtu.be/IrJmuow1r7g?t=3007


class InitialPoseSetter(Node):
    def __init__(self):
        super().__init__('initial_pose_setter')
        self.client = self.create_client(SetInitialPose, 'set_initial_pose')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        self.set_initial_pose()

    def set_initial_pose(self):
        request = SetInitialPose.Request()
        pose = PoseWithCovarianceStamped()
        
        # Set the position
        pose.header.frame_id = 'map'  # or 'odom' depending on your frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.pose.position.x = 1.0  # Set your desired x position
        pose.pose.pose.position.y = 2.0  # Set your desired y position
        pose.pose.pose.position.z = 0.0  # Usually 0 for 2D navigation
        
        # Set the orientation (quaternion)
        pose.pose.pose.orientation.x = 0.0  # Set your desired orientation
        pose.pose.pose.orientation.y = 0.0
        pose.pose.pose.orientation.z = 0.707  # Example value
        pose.pose.pose.orientation.w = 0.707  # Example value
        
        pose.pose.covariance = [0.0] * 36  # Set covariance if needed
        request.pose = pose
        
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Initial pose set successfully')
        else:
            self.get_logger().error('Failed to set initial pose')

def main(args=None):
    rclpy.init(args=args)
    initial_pose_setter = InitialPoseSetter()
    rclpy.spin(initial_pose_setter)
    initial_pose_setter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()