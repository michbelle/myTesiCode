import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch.conditions import IfCondition

from launch.actions import ExecuteProcess

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
    
    headless = LaunchConfiguration("headless")
    headless_dcl = DeclareLaunchArgument(
        'headless',
        default_value='True')
    
    
    gz_world_arg = PathJoinSubstitution([
        '/root/ff_ws/src/myTesiCode/rmf_code/ign_world', world])

    # Include the gz sim launch file  
    gz_sim_share = get_package_share_directory("ros_gz_sim")
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-s', gz_world_arg],
        output='screen',
    )
    
    gz_sim_gui = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz_sim_share, "launch", "gz_sim.launch.py")),
        condition=IfCondition(PythonExpression(["not ", headless])),
        launch_arguments={
            "gz_args" : ["-v4 -g "],
        }.items(),
    )
    
    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(headless_dcl)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_world_cmd)

    # Launch Gazebo
    ld.add_action(gz_sim)
    ld.add_action(gz_sim_gui)

    return ld
