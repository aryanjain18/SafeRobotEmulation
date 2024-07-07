# Prerequisites

Ubuntu 20.04
ROS2 foxy
OpenCV 4.2.0
CARLA with Ros bridge

Build ORB_SLAM3 : https://github.com/zang09/ORB-SLAM3-STEREO-FIXED

Clone the repository:

    git clone https://github.com/zang09/ORB-SLAM3-STEREO-FIXED.git ORB_SLAM3
    
Install same required dependencies as original version. Then,
Execute:

    cd ORB_SLAM3
    chmod +x build.sh
    ./build.sh
    
This will create libORB_SLAM3.so at lib folder and the executables in Examples folder.

# Building ORBSLAM3 with ROS2 

https://github.com/zang09/ORB_SLAM3_ROS2

Clone repository to your ROS workspace
>      mkdir -p colcon_ws/src
>      cd ~/colcon_ws/src
>      git clone https://github.com/zang09/ORB_SLAM3_ROS2.git orbslam3_ros2

Change this line at CMakeLists.txt to your own python site-packages path

    set(ENV{PYTHONPATH}"/opt/ros/foxy/lib/python3.8/site-packages/")

Change this CMakeModules/FindORB_SLAM3.cmake to your own ORB_SLAM3 path

    set(ORB_SLAM3_ROOT_DIR"~/Install/ORB_SLAM/ORB_SLAM3")
    
Now Build :

     cd ~/colcon_ws
     colcon build --symlink-install --packages-select orbslam3

**Troubleshootings:**

If you cannot find sophus/se3.hpp:
Go to your ORB_SLAM3_ROOT_DIR and install sophus library.

    cd ~/{ORB_SLAM3_ROOT_DIR}/Thirdparty/Sophus/build
     sudo make install
     
# How to use

Source the workspace

    $ source ~/colcon_ws/install/local_setup.bash
    
**NOTE** : In the Examples_old/ROS/ORB_SLAM3/src update the topics of the mode you want to use for example in Monocular change the ros_mono.cc line 62 : ros::Subscriber sub = nodeHandler.subscribe("/camera/image_raw", 1, &ImageGrabber::GrabImage,&igb); with the relevant topic that your carla vehicle is publishing.
 


Run orbslam mode, which you want.

You can find vocabulary file and config file in here. (e.g. orbslam3_ros2/vocabulary/ORBvoc.txt, orbslam3_ros2/config/monocular/TUM1.yaml for monocular SLAM).

MONO mode

    $ ros2 run orbslam3 mono PATH_TO_VOCABULARY PATH_TO_YAML_CONFIG_FILE
STEREO mode

    $ ros2 run orbslam3 stereo PATH_TO_VOCABULARY PATH_TO_YAML_CONFIG_FILE BOOL_RECTIFY
RGBD mode

    $ ros2 run orbslam3 rgbd PATH_TO_VOCABULARY PATH_TO_YAML_CONFIG_FILE
STEREO-INERTIAL mode

    $ ros2 run orbslam3 stereo-inertial PATH_TO_VOCABULARY PATH_TO_YAML_CONFIG_FILE BOOL_RECTIFY [BOOL_EQUALIZE]


**NOTE** : Create a seperate instance for each of the multiple vehicles in your setup to perform seperate online ORBSLAM3 on each of them together.