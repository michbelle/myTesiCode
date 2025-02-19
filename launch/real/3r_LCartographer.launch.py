import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from nav2_common.launch import RewrittenYaml
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory



def generate_launch_description():
    # Positioning function pack
    pkg_share = FindPackageShare(package='myCode').find('myCode')#ugv02_cartographer

    # Configure node launch information
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    # Map resolution
    resolution = LaunchConfiguration('resolution', default='0.05')
    # Map publish period
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='0.5')
    # load_state_arg = LaunchConfiguration('load_state_filename')
    # Configuration file folder path
    configuration_directory = LaunchConfiguration('configuration_directory',default= os.path.join(pkg_share, 'config') )
    # Configuration file
    configuration_basename = LaunchConfiguration('configuration_basename', default='localizationCartographer.lua') # localizationCartographer cartographer_example

    load_state_filename_arg = LaunchConfiguration('load_state_filename', default= os.path.join(pkg_share, 'maps', "map-elettra/Cart/map.pbstream"))


    #Nodes
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        remappings=[
                ('/odom', '/odometry/filtered'),  # Remap odom to /odometry/filtered
                ('/imu', '/imu/data'),  # Remap odom to /odometry/filtered
            ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-configuration_directory', configuration_directory,
                   '-configuration_basename', configuration_basename,
                   '-load_state_filename', load_state_filename_arg])

    cartographer_occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        remappings=[
                ('/odom', '/odometry/filtered'),  # Remap odom to /odometry/filtered
                ('/imu', '/imu/data'),  # Remap odom to /odometry/filtered
            ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-resolution', resolution, '-publish_period_sec', publish_period_sec])

    # adding map server

    # bringup_dir = get_package_share_directory('myCode')


    # namespace = LaunchConfiguration('namespace',  default='')
    # # map_yaml_file = LaunchConfiguration('map', default=os.path.join(bringup_dir, 'config', 'mapServer_config.yaml'))
    # map_yaml_file = LaunchConfiguration('map', default=os.path.join(bringup_dir, 'maps', 'maze_cart.yaml'))
    # autostart = LaunchConfiguration('autostart',default='true')

    # # namespace_L = DeclareLaunchArgument(
    # #     'namespace', default_value='',
    # #     description='Top-level namespace'),

    # # Map_L = DeclareLaunchArgument(
    # #     'map',
    # #     default_value=os.path.join(bringup_dir, 'config', 'mapServer_config.yaml'),
    # #     description='Full path to map yaml file to load'),

    # # autostart_L = DeclareLaunchArgument(
    # #     'autostart', default_value='true',
    # #     description='Automatically startup the nav2 stack'),

    # lifecycle_nodes = ['map_server']

    # remappings = [('/tf', 'tf'),
    #               ('/tf_static', 'tf_static')]

    # nodeMapServer = Node(
    #     package='nav2_map_server',
    #     executable='map_server',
    #     name='map_server',
    #     output='screen',
    #     parameters=[{"yaml_filename": map_yaml_file}],
    #     remappings=remappings)


    # nodeLifeManager = Node(
    #     package='nav2_lifecycle_manager',
    #     executable='lifecycle_manager',
    #     name='lifecycle_manager_localization',
    #     output='screen',
    #     parameters=[{'use_sim_time': use_sim_time},
    #                 {'autostart': autostart},
    #                 {'node_names': lifecycle_nodes}])




    #Launch file
    ld = LaunchDescription()
    # ld.add_action(load_state_filename_arg)
    ld.add_action(cartographer_node)
    ld.add_action(cartographer_occupancy_grid_node)


    
    # ld.add_action(namespace_L)
    # ld.add_action(Map_L)
    # ld.add_action(autostart_L)
    # ld.add_action(nodeMapServer)
    # ld.add_action(nodeLifeManager)


    return ld