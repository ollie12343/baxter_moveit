source /opt/ros/kinetic/setup.sh

rosdep install -y -i --from-path src --ignore-src --rosdistro kinetic

catkin_make

source devel/setup.bash