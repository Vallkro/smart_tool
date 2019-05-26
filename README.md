# smart_tool
Smart oil filter tool  capstone project

Also add this as a startup script:

#! /bin/bash
echo 298 > /sys/class/gpio/export 
echo 388 > /sys/class/gpio/export 
source ~/ros2_ws/install/setup.*
source ~/ros2_ws/install/local_setup.bash
ros2 run smart_tool listener
