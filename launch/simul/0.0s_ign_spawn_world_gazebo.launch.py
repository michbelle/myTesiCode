import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue



def generate_launch_description():
    # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')
    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')
    
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value='elettra/ign-elettra-map.world',
        description='World file to use in Gazebo')
    
    gz_world_arg = PathJoinSubstitution([
        '/root/ff_ws/src/myTesiCode/rmf_code/ign_world', world])

    # Include the gz sim launch file  
    gz_sim_share = get_package_share_directory("ros_gz_sim")
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz_sim_share, "launch", "gz_sim.launch.py")),
        launch_arguments={
            "gz_args" : gz_world_arg,
            "headless": "true"
        }.items()
    )
    
    # Spawn Rover Robot
    gz_spawn_entity_rover_mini = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "/rover_mini/robot_description",
            "-name", "rover_mini",
            "-allow_renaming", "true",
            "-x", "53.84",
            "-y","-62.60",
            "-z", "0.1",
        ]
    )
    
    # Spawn Rover Robot
    gz_spawn_entity_jobot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "/jobot/robot_description",
            "-name", "jobot",
            "-allow_renaming", "true",
            "-x", "53.84",
            "-y","-62.60",
            "-z", "0.1",
        ]
    )
    
    gz_ros2_bridge_rover_mini = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/odometry/wheels@nav_msgs/msg/Odometry@ignition.msgs.Odometry",
            "/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
        ],
    )

    
    gz_ros2_bridge_jobot = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
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
    
    urdf = os.path.join(get_package_share_directory(
        'myCode'), 'urdf', 'mini.urdf')

    robot_desc = ParameterValue(Command(['xacro ', urdf]),
                                       value_type=str)

    # Robot state publisher
    params = {'use_sim_time': use_sim_time, 'robot_description': robot_desc}
    start_robot_state_publisher_cmd = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params],
            arguments=[])
    

    urdf = os.path.join(get_package_share_directory(
        'jobot_simulation'), 'model',"urdf", 'jobot_robot.urdf')

    robot_desc = ParameterValue(Command(['xacro ', urdf]),
                                       value_type=str)
    # Robot state publisher
    params = {'use_sim_time': use_sim_time, 'robot_description': robot_desc}
    start_robot_state_publisher_cmd = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params],
            arguments=[])

    
    rviz_config_dir = os.path.join(
            get_package_share_directory('myCode'),
            'rviz',
            'default.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        output='screen')


    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_world_cmd)

    # Launch Gazebo
    ld.add_action(gz_sim)
    ld.add_action(gz_spawn_entity)
    ld.add_action(gz_ros2_bridge)


    # Launch Robot State Publisher
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(rviz_node)

    return ld
