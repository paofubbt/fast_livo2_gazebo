# gazebo_car
用于测试fast-livo2的仿真
# 需要依赖包
```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros ros-humble-turtlebot3-description ros-humble-turtlebot3-gazebo ros-humble-robot-state-publisher ros-humble-xacro ros-humble-rviz2
```
# 操作
## 启动仿真节点
```bash
ros2 launch turtlebot3_custom spawn_robot_with_plugins.launch.py
```
## 启动控制运动节点
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**注意控制键为 u i o j k l**

## 其中fast-livo2配置文件为针对仿真小车的配置文件
- 启动fast-livo2
```bash
ros2 launch fast_livo fast_livo_sim_display.launch.py
```
