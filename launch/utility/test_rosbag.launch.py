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

    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    # Include the gz sim launch file  
    launch_folder = get_package_share_directory("myCode")
    rvizvisu = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "utility", "test_ekf_loc_Wsensors.launch.py")),
        launch_arguments={
        }.items()
    )

    # rosbagNode = Node(
    #         package='rosbag2',  # Package that contains the rosbag2 play node
    #         executable='rosbag2_play',  # Executable for playing bag files
    #         name='rosbag2_play',
    #         output='screen',
    #         parameters=[{
    #             'use_sim_time': True,  # Use simulation time
    #         }],
    #         # arguments=['/root/ff_ws/src/bag_files/record_001', '--clock', "--delay", "5.0"],
    #     ),

    odometry_increase_precision = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul", "1s_robot_localizationEKF.launch.py")),
        launch_arguments={
        }.items()
    )

    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul","2s_navigation.launch.py")),
        launch_arguments={
        }.items()
    )

    localization_nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul","3s_Lamcl.launch.py")),
        launch_arguments={
        }.items()
    )



    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)

    # Launch Gazebo
    ld.add_action(rvizvisu)
    # ld.add_action(rosbagNode)
    ld.add_action(odometry_increase_precision)
    ld.add_action(nav_launch)
    ld.add_action(localization_nav)

    return ld
