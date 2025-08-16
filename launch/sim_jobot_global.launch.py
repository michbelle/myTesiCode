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
    # Create the launch configuration variables
    set_env_id_jobot=SetEnvironmentVariable('ROS_DOMAIN_ID', '20'),
    use_sim_time = LaunchConfiguration('use_sim_time')

    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    # Include the gz sim launch file  
    launch_folder = get_package_share_directory("myCode")
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul", "0.2s_ign_spawn_jobot_gazebo.launch.py")),
        launch_arguments={
        }.items()
    )
    
    launch_folder = get_package_share_directory("jobot_launchpad")
    odometry_increase_precision = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul", "Slocalization.launch.py")),
        launch_arguments={
        }.items()
    )

    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul", "Snavigation.launch.py")),
        launch_arguments={
        }.items()
    )

    localization_nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch", "simul", "Sslam.py")),
        launch_arguments={
        }.items()
    )



    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(set_env_id_jobot)

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)

    # Launch Gazebo
    ld.add_action(gz_sim)
    ld.add_action(odometry_increase_precision)
    ld.add_action(nav_launch)
    ld.add_action(localization_nav)

    return ld
