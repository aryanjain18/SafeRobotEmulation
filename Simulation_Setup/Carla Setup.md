# **System requirements**

* Ubuntu 18.04. CARLA provides support for previous Ubuntu versions up to 16.04. However proper compilers are needed for Unreal Engine to work properly. Dependencies for Ubuntu 18.04 and previous versions are listed separately below. Make sure to install the ones corresponding to your system.
* 130 GB disk space. Carla will take around 31 GB and Unreal Engine will take around 91 GB so have about 130 GB free to account for both of these plus additional minor software installations.
* An adequate GPU. CARLA aims for realistic simulations, so the server needs at least a 6 GB GPU although 8 GB is recommended. A dedicated GPU is highly recommended for machine learning.
* Two TCP ports and good internet connection. 2000 and 2001 by default. Make sure that these ports are not blocked by firewalls or any other applications.

## **Software requirements :**
## 
CARLA requires many different kinds of software to run. Some are built during the CARLA build process itself, such as Boost.Python. Others are binaries that should be installed before starting the build (cmake, clang, different versions of Python, etc.). To install these requirements, run the following commands:

    sudo apt-get update &&
    sudo apt-get install wget software-properties-common &&
    sudo add-apt-repository ppa:ubuntu-toolchain-r/test &&
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add

    Download the appropriate package (here 0.9.13) for your desired version of CARLA.
    https://github.com/carla-simulator/carla/blob/master/Docs/download.md
    
Ubuntu 22.04.

    sudo apt-add-repository "deb http://archive.ubuntu.com/ubuntu focal main universe"
    sudo apt-get update
    sudo apt-get install build-essential clang-10 lld-10 g++-7 cmake ninja-build libvulkan1 python python3 python3-dev python3-pip libpng-dev libtiff5-dev libjpeg-dev tzdata sed curl unzip autoconf libtool rsync libxml2-dev git git-lfs
    sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-10/bin/clang++ 180 &&
    sudo update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-10/bin/clang 180 &&
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 180

Ubuntu 20.04.

    sudo apt-add-repository "deb http://apt.llvm.org/focal/ llvm-toolchain-focal main"
    sudo apt-get update
    sudo apt-get install build-essential clang-10 lld-10 g++-7 cmake ninja-build libvulkan1 python python-dev python3-dev python3-pip libpng-dev libtiff5-dev libjpeg-dev tzdata sed curl unzip autoconf libtool rsync libxml2-dev git
    sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-10/bin/clang++ 180 &&
    sudo update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-10/bin/clang 180



Ubuntu 18.04.

    sudo apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic main"
    sudo apt-get update
    sudo apt-get install build-essential clang-8 lld-8 g++-7 cmake ninja-build libvulkan1 python python-pip python-dev python3-dev python3-pip libpng-dev libtiff5-dev libjpeg-dev tzdata sed curl unzip autoconf libtool rsync libxml2-dev git
    sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-8/bin/clang++ 180 &&
    sudo update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-8/bin/clang 180

# **NOTE:** 
#     
> You may require a Unreal Engine acocunt if you're setting up Carla or using the Unreal Engine platform in your system for the first time. 

Starting with version 0.9.12, CARLA uses a modified fork of Unreal Engine 4.26. This fork contains patches specific to CARLA.
    
To download this fork of Unreal Engine, you need to have a GitHub account linked to Unreal Engine's account.
    
Follow the guide in this link : 
https://www.unrealengine.com/en-US/ue-on-github
    
(summarized version):

**Link Accounts**
1. Open your Epic Game account dashboard, hover over your username, and select the Personal button from the drop-down menu.
1. With your account dashboard open, select the Connections tab from the sidebar.
1. After opening the Connections menu, select the Accounts tab, and then select the Connect button below the GitHub icon.
1. Select the Unreal Engine End User License Agreement (EULA) appropriate for your needs and read through the terms, then select the Link Account button.
1. To complete the OAuth App Authorization process, click the Authorize EpicGames button.
1. GitHub will send an email inviting you to join the @EpicGames organization on GitHub. You must select the Join @EpicGames button in this email within seven days to complete the GitHub and Epic Games account linking process.
1. Upon completion, you will receive an email from Epic Games verifying that your GitHub and Epic Games accounts were successfully linked. 

Once the setup is done : 

1. Clone the content for CARLA's fork of Unreal Engine 4.26 to your local computer:

        git clone --depth 1 -b carla https://github.com/CarlaUnreal/UnrealEngine.git ~/UnrealEngine_4.26
2. Navigate into the directory where you cloned the repository:

        cd ~/UnrealEngine_4.26
3. Make the build. This may take an hour or two depending on your system.

        ./Setup.sh && ./GenerateProjectFiles.sh && make
4. Open the Editor to check that Unreal Engine has been installed properly.

        cd ~/UnrealEngine_4.26/Engine/Binaries/Linux && ./UE4Editor
    

# CARLA 
# 

Clone the CARLA repository

        git clone https://github.com/carla-simulator/carla

For our use clone the **0.9.13 branch**


# Get assets

Run the following command in the CARLA root folder:

        ./Update.sh
        
The assets will be downloaded and extracted to the appropriate location

To download the assets for a specific version of CARLA:

1. From the root CARLA directory, navigate to /Util/ContentVersions.txt. This document contains the links to the assets for all CARLA releases.
1. Extract the assets in Unreal\CarlaUE4\Content\Carla. If the path doesn't exist, create it.
1. Extract the file with a command similar to the following:

        tar -xvzf <assets_file_name>.tar.gz.tar -C /path/to/carla/Unreal/CarlaUE4/Content/Carla

# Set Unreal Engine environment variable

To set the variable for this session only:

    export UE4_ROOT=~/UnrealEngine_4.26
To set the variable so it persists across sessions:

1. Open ~/.bashrc or ./profile.

        gedit ~/.bashrc
        or 
        gedit ~/.profile
2. Add the following line to the bottom of the file:

        export UE4_ROOT=~/UnrealEngine_4.26 
    
3. Save the file and reset the terminal.

# Build CARLA

**All commands should be run in the root CARLA folder.**

There are two parts to the build process for CARLA, compiling the client and compiling the server.

Compile the Python API client:
            
            make PythonAPI
            
For Specific version : 

    ARGS="--python-version=2.7, 3.6, 3.7, 3.8"

# CARLA client library :
#     
The CARLA client library will be built in two distinct, mutually exclusive forms. This gives users the freedom to choose which form they prefer to run the CARLA client code. The two forms include .egg files and .whl files. Choose one of the following options below to use the client library:

A. .egg file

The .egg file does not need to be installed. All of CARLA's example scripts automatically look for this file when importing CARLA.

If you previously installed a CARLA .whl, the .whl will take precedence over an .egg file.

B. .whl file

The .whl file should be installed using pip or pip3:

# Python 3
    pip3 install <path/to/wheel>.whl

# Python 2
    pip install <path/to/wheel>.whl
This .whl file cannot be distributed as it is built specifically for your OS.

# Compile the server:
# 
The following command compiles and launches Unreal Engine. Run this command each time you want to launch the server or use the Unreal Engine editor:

    make launch
The project may ask to build other instances such as UE4Editor-Carla.dll the first time. Agree in order to open the project. During the first launch, the editor may show warnings regarding shaders and mesh distance fields. These take some time to be loaded and the map will not show properly until then.

# Example :
# 

 Start the simulation:

Press Play to start the server simulation. The camera can be moved with WASD keys and rotated by clicking the scene while moving the mouse around.

Test the simulator using the example scripts inside PythonAPI\examples. With the simulator running, open a new terminal for each script and run the following commands to spawn some life into the town and create a weather cycle:

        # Terminal A 
        cd PythonAPI/examples
        python3 -m pip install -r requirements.txt
        python3 generate_traffic.py  

        # Terminal B
        cd PythonAPI/examples
        python3 dynamic_weather.py 
