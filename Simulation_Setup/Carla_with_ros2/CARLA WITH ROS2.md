# **ROS bridge installation for ROS 2**
# 

# Install ROS

ROS 2 Foxy — For Ubuntu 20.04 (Focal)

https://docs.ros.org/en/foxy/Installation.html

# System setup
#
**Set locale**

Make sure you have a locale which supports UTF-8. If you are in a minimal environment (such as a docker container), the locale may be something minimal like POSIX. We test with the following settings. However, it should be fine if you’re using a different UTF-8 supported locale.

    locale  # check for UTF-8

    sudo apt update && sudo apt install locales
    sudo locale-gen en_US en_US.UTF-8
    sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
    export LANG=en_US.UTF-8

    locale  # verify settings

**Add the ROS 2 apt repository**

    sudo apt install software-properties-common
    sudo add-apt-repository universe
    
**Add the ROS 2 GPG key with apt**

    sudo apt update && sudo apt install curl -y
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
    
 **Add the repository to your sources list**
 
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    
# Install development tools and ROS tools

    sudo apt update && sudo apt install -y \
      libbullet-dev \
      python3-pip \
      python3-pytest-cov \
      ros-dev-tools

    # install some pip packages needed for testing
    python3 -m pip install -U \
      argcomplete \
      flake8-blind-except \
      flake8-builtins \
      flake8-class-newline \
      flake8-comprehensions \
      flake8-deprecated \
      flake8-docstrings \
      flake8-import-order \
      flake8-quotes \
      pytest-repeat \
      pytest-rerunfailures \
      pytest
    # install Fast-RTPS dependencies
    sudo apt install --no-install-recommends -y \
      libasio-dev \
      libtinyxml2-dev
    # install Cyclone DDS dependencies
    sudo apt install --no-install-recommends -y \
      libcunit1-dev

**Get ROS 2 code**

Create a workspace and clone all repos:

    mkdir -p ~/ros2_foxy/src
    cd ~/ros2_foxy
    vcs import --input https://raw.githubusercontent.com/ros2/ros2/foxy/ros2.repos src
    
**Install dependencies using rosdep**

    sudo apt upgrade
    sudo rosdep init
    rosdep update
    rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-5.3.1 urdfdom_headers"

**Build the code in the workspace**

    cd ~/ros2_foxy/
    colcon build --symlink-install

# Environment setup

Set up your environment by sourcing the following file.

    # Replace ".bash" with your shell if you're not using bash
    # Possible values are: setup.bash, setup.sh, setup.zsh
    . ~/ros2_foxy/install/local_setup.bash
    
# Example

In one terminal, source the setup file and then run a C++ talker:

    . ~/ros2_foxy/install/local_setup.bash
    ros2 run demo_nodes_cpp talker
    
In another terminal source the setup file and then run a Python listener:

    . ~/ros2_foxy/install/local_setup.bash
    ros2 run demo_nodes_py listener
    
You should see the talker saying that it’s Publishing messages and the listener saying I heard those messages. This verifies both the C++ and Python APIs are working properly.

# ROS bridge installation

Set up the project directory and clone the ROS bridge repository and submodules:

    mkdir -p ~/carla-ros-bridge && cd ~/carla-ros-bridge
    git clone --recurse-submodules https://github.com/carla-simulator/ros-bridge.git src/ros-bridge

Set up the ROS environment:

    source /opt/ros/foxy/setup.bash

Install the ROS dependencies:

    rosdep update
    rosdep install --from-paths src --ignore-src -r

Build the ROS bridge workspace using colcon:

    colcon build

# Run the ROS bridge

Start a CARLA server according to the installation method used to install CARLA:

    # Package version in carla root folder
    ./CarlaUE4.sh

    # Debian installation in `opt/carla-simulator/`
    ./CarlaUE4.sh

    # Build from source version in carla root folder
    make launch
    
Add the correct CARLA modules to your Python path:

    export CARLA_ROOT=<path-to-carla>
    export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-<carla_version_and_arch>.egg:$CARLA_ROOT/PythonAPI/carla
    
Add the source path for the ROS bridge workspace:

    source ./install/setup.bash
    
 In another terminal, start the ROS 2 bridge. You can run one of the two options below:

    # Option 1, start the basic ROS bridge package
    ros2 launch carla_ros_bridge carla_ros_bridge.launch.py

    # Option 2, start the ROS bridge with an example ego vehicle
    ros2 launch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch.py
    

**FOR OUR CURRENT SYSTEM :** 

Start the basic ROS bridge : 

    # Option 1, start the basic ROS bridge package
    ros2 launch carla_ros_bridge carla_ros_bridge.launch.py
    
Add our custom spawn object.json files : 

    ros2 launch carla_spawn_objects carla_spawn_objects.launch.py objects_definition_file:=path/to/objects.json
    
Add & Run the Manual Control script for both the vehicles : 

     ros2 launch carla_manual_control carla_manual_control.launch.py
     
To steer the vehicle manually, press 'B'. Press 'H' to see instructions

Add the Visualisation files and in seperate  Rviz2 instances call them they would be something like :

    ros-bridge/carla/config/carla.rviz



