cmake_minimum_required(VERSION 3.0.2)
project(ping1d)

find_package(catkin REQUIRED COMPONENTS rospy std_msgs message_generation sensor_msgs)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  PingRange.msg
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
  std_msgs
  message_runtime
)

include_directories( ${catkin_INCLUDE_DIRS})
catkin_install_python(PROGRAMS
  scripts/driver.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
