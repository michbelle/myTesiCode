#!/usr/bin/env python3

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from math import pi

def generate_launch_description():

    # Start robot localization using an Extended Kalman filter
    config_path = Path(get_package_share_directory(
        'myCode'), 'config', 'utility', 'odom_config.yaml')
    
    localization_node = Node(
    	package='myCode',
    	executable='record_odom_data.py',
    	name='odom_print',
    	output='screen',
    	parameters=[config_path]
    	)
    
    ld = LaunchDescription()

    ld.add_action(localization_node)

    return ld

