cmake_minimum_required(VERSION 3.8)
project(turtlebot3_custom)

# 默认使用C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# 查找ament_cmake
find_package(ament_cmake REQUIRED)

# 查找依赖包
find_package(ament_cmake REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(turtlebot3_description REQUIRED)
find_package(turtlebot3_gazebo REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(xacro REQUIRED)

# 安装目录
install(
  DIRECTORY models launch worlds config rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
