from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition

def generate_launch_description():

    # ----- Launch arguments
    use_sim_time      = LaunchConfiguration('use_sim_time')
    use_ros2_control  = LaunchConfiguration('use_ros2_control')
    use_gazebo        = LaunchConfiguration('use_gazebo')

    # ----- Directories
    pkg_share = get_package_share_directory('description')
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'side1.urdf'])

    robot_description_content = Command([
        'xacro ', xacro_file,
        ' use_ros2_control:=', use_ros2_control,
        ' use_gazebo:=', use_gazebo
    ])
    robot_description = ParameterValue(robot_description_content, value_type=str)
    
    # ----- Nodes
    rs_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters= [{
            'robot_description': robot_description,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'use_ros2_control': LaunchConfiguration('use_ros2_control'),
            'use_gazebo': LaunchConfiguration('use_gazebo')
        }]
    )
    
    # If we are not using ros2 control, initialize the gui for joint manipulation
    # Else, we do not need the gui as something else will control the rover
    gui_js = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }],
        condition=IfCondition(LaunchConfiguration('use_js_gui'))
    )


    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('use_ros2_control', default_value='false'),
        DeclareLaunchArgument('use_gazebo', default_value='false'),
        DeclareLaunchArgument('use_js_gui', default_value='false'),

        rs_pub,
        gui_js
    ])