#!/usr/bin/python3
# -- coding: utf-8 --**

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    
    # 路径
    config_file_dir = os.path.join(get_package_share_directory("fast_livo"), "config")
    rviz_config_file = os.path.join(get_package_share_directory("fast_livo"), "rviz_cfg", "fast_livo2.rviz")

    # 配置文件
    sim_config_cmd = os.path.join(config_file_dir, "sim_livo_display.yaml")
    camera_config_cmd = os.path.join(config_file_dir, "camera_pinhole.yaml")

    # 参数声明
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="True",
    )
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
    )
    use_respawn_arg = DeclareLaunchArgument(
        'use_respawn', 
        default_value="True",
    )

    # 参数获取
    use_respawn = LaunchConfiguration('use_respawn')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        use_rviz_arg,
        use_sim_time_arg,
        use_respawn_arg,

        # FAST-LIVO2 主节点 (LIVO模式)
        Node(
            package="fast_livo",
            executable="fastlivo_mapping",
            name="laserMapping",
            parameters=[
                sim_config_cmd,          # 主参数文件，包含VIO配置
                camera_config_cmd,       # 相机内参文件
                {"use_sim_time": use_sim_time}
            ],
            output="screen",
            respawn=use_respawn,
        ),

        # RViz
        Node(
            condition=IfCondition(use_rviz),
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_file],
            parameters=[{"use_sim_time": use_sim_time}],
            output="screen"
        ),
    ])
