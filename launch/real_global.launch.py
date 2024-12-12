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
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    # Include the gz sim launch file  
    launch_folder = get_package_share_directory("myCode")

    control_hw_mini = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch/real", "sensorLaunch.launch.py")),
        launch_arguments={
        }.items()
    )

    activate_sensors = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch/real", "sensorLaunch.launch.py")),
        launch_arguments={
        }.items()
    )


    odometry_increase_precision = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch/real", "1r_robot_localizer.launch.py")),
        launch_arguments={
        }.items()
    )

    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch/real", "2r_navigation_launch.py")),
        launch_arguments={
        }.items()
    )

    localization_nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_folder, "launch/real", "3r_slam_launch.py")),
        launch_arguments={
        }.items()
    )



    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)

    ld.add_action(control_hw_mini)
    ld.add_action(activate_sensors)
    ld.add_action(odometry_increase_precision)
    ld.add_action(nav_launch)
    ld.add_action(localization_nav)

    return ld
