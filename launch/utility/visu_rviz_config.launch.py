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

    robot_name="jobot1"


    # Robot state publisher

    # urdf = os.path.join(get_package_share_directory(
    #     "myCode"), "urdf", "mini.urdf")
    # robot_desc = ParameterValue(Command(["xacro ", urdf]),
    #                                    value_type=str)
    # params = {"use_sim_time": use_sim_time, "robot_description": robot_desc}
    # start_robot_state_publisher_cmd = Node(
    #         package="robot_state_publisher",
    #         executable="robot_state_publisher",
    #         name=robot_name+"_state_publisher",
    #         output="screen",
    #         # namespace=robot_name,
    #         parameters=[params],
    #         # remappings=[
    #         #     ("/tf", "/mini/tf"),
    #         #     ("/tf_static", "/mini/tf_static"),
    #         # ],
    #         arguments=[])

    # gen rviz

    rviz_config_dir = os.path.join(
            get_package_share_directory("myCode"),
            "rviz", "nav",
            "test.rviz")
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2_mini_nav",
        arguments=["-d", rviz_config_dir],
        output="screen")



    # Create the launch description and populate
    ld = LaunchDescription()

    # ld.add_action(set_env_id_mini)

    # Declare the launch options

    # Launch Robot State Publisher
    # ld.add_action(start_robot_state_publisher_cmd) {}
    ld.add_action(rviz_node)

    return ld
