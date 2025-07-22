import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # ----- Directories
    pkg_description = get_package_share_directory('description')
    rviz_config_file = PathJoinSubstitution([pkg_description, 'rviz', 'view_model_config.rviz'])


    # ----- Nodes
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([PathJoinSubstitution([(pkg_description), 'launch', 'robot_state_publisher.launch.py'])]),
        launch_arguments={
            'use_sim_time': 'false',
            'use_ros2_control': 'false',
            'use_gazebo': 'false',
            'use_js_gui':'true'
            }.items()
    )

    rviz = Node(
                package='rviz2',
                executable='rviz2',
                output='screen',
                arguments=['-d', rviz_config_file]
                )

    return LaunchDescription([
        rsp,
        rviz
    ])
