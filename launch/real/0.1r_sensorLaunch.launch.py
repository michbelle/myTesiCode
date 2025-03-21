#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

laserTTYinfo=['10c4', 'ea60']
# imuTTYinfo=['0403','6001'] # FT232RL
imuTTYinfo=['0403','6014'] # FT232H

def getttyusbconnected(vendorID:str, productID:str)->str:
    import pyudev

    context = pyudev.Context()

    # Iterate over all devices in the system
    for device in context.list_devices(subsystem='tty'):
        # Check if the device has the correct vendor and product ID
        if device.get('ID_VENDOR_ID') == vendorID and device.get('ID_MODEL_ID') == productID:
            return str(device.device_node)
    else:
        raise ValueError('Device not found')



def generate_launch_description():
    ld = LaunchDescription()

    pathlaser = getttyusbconnected(*laserTTYinfo)

    sllidar_ros2 = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('myCode'), 
                "launch/sensor", 
                "sllidar_s1_launch.py")),
            launch_arguments={
            "serial_port" : pathlaser,
            "frame_id" : 'laser'
            }.items(),
        )
    
    info_msg_laser = LogInfo(msg=f"laser found in {pathlaser}")

    pathimu = getttyusbconnected(*imuTTYinfo).split("/")[-1]

    imu_ros2 = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('myCode'), 
                "launch/sensor", 
                "wt901.launch.py")),
            launch_arguments={
            "port" : pathimu
            }.items(),
        )
    
    info_msg_imu = LogInfo(msg=f"imu found in {pathimu}")
    
    ld.add_action(sllidar_ros2)
    ld.add_action(info_msg_laser)
    ld.add_action(imu_ros2)
    ld.add_action(info_msg_imu)
    return ld