import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import FindExecutable, Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 包路径
    pkg_turtlebot3_custom = get_package_share_directory('turtlebot3_custom')

    # ====================== 关键修复：让 Gazebo 找到模型 ======================
    # 你的模型文件夹路径（必须包含 house 等环境模型）
    model_path = os.path.join(pkg_turtlebot3_custom, 'models')

    # 设置环境变量：把你的模型路径加入 GAZEBO_MODEL_PATH
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=model_path + os.pathsep + os.environ.get('GAZEBO_MODEL_PATH', '')
    )
    # =========================================================================

    # 生成完整的机器人描述（包含Gazebo插件）
    robot_description_content = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            pkg_turtlebot3_custom,
            'models/urdf',
            'turtlebot3_waffle_pi_3d_combined.urdf.xacro'
        ])
    ])

    robot_description = {'robot_description': robot_description_content}

    # 启动Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([
                pkg_turtlebot3_custom, 'worlds', 'turtlebot3_house.world'
            ]),
            'verbose': 'true'
        }.items()
    )

    # 机器人状态发布器
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    # 在Gazebo中生成机器人
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'turtlebot3_3d_with_plugins',
            '-x', '-2.0',
            '-y', '-1.0',
            '-z', '0.1',
            '-Y', '0.0'
        ],
        output='screen'
    )

    # 启动键盘控制（可选）
    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        parameters=[{
            'speed_linear': 0.001,
            'speed_angular': 0.0025
        }]
    )

    return LaunchDescription([
        # 关键：先设置模型路径，再启动Gazebo
        set_gazebo_model_path,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        # teleop
    ])

