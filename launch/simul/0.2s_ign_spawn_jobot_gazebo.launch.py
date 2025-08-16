import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    
    
    set_env_id_jobot=SetEnvironmentVariable('ROS_DOMAIN_ID', '20'),
    # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')
    
    # Spawn Rover Robot
    gz_spawn_entity_jobot = Node(
        package="ros_gz_sim",
        executable="create",
        name='jobot_gz_create',
        arguments=[
            "-topic", "/jobot/robot_description",
            "-name", "jobot",
            "-allow_renaming", "true",
            "-x", "53.84",
            "-y","-62.60",
            "-z", "0.1",
        ]
    )
    
    gz_ros2_bridge_jobot = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name='jobot_gz_bridge',
        arguments=[
            "/jobot/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/jobot/odometry/wheels@nav_msgs/msg/Odometry@ignition.msgs.Odometry",
            "/jobot/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            '/jobot/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/jobot/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/jobot/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
        ],
    )

    # Robot state publisher
        
    urdf = os.path.join(get_package_share_directory(
        'jobot_simulation'), "model",'urdf', 'jobot_robot.urdf')
    robot_desc = ParameterValue(Command(['xacro ', urdf]),
                                       value_type=str)
    params = {'use_sim_time': use_sim_time, 'robot_description': robot_desc}
    start_robot_state_publisher_cmd = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='jobot_state_publisher',
            output='screen',
            parameters=[params],
            arguments=[])
    
    # gen rviz
    
    rviz_config_dir = os.path.join(
            get_package_share_directory('myCode'),
            'rviz', 'nav',
            'jobot_nav.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_jobot_nav',
        arguments=['-d', rviz_config_dir],
        output='screen')


    # Create the launch description and populate
    ld = LaunchDescription()
    
    ld.add_action(set_env_id_jobot)

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)

    #add robot
    ld.add_action(gz_spawn_entity_jobot)
    ld.add_action(gz_ros2_bridge_jobot)

    # Launch Robot State Publisher
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(rviz_node)

    return ld
