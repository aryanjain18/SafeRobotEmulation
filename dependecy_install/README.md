# Spinnaker and PySpin Installation
The repository contains the source code and required file for installation of Spinnakeer and Pyspin dependencies.

## Table of Contents
1. [Spinnaker Setup](#spinnaker-setup)
2. [PySpin Setup](#pyspin-setup)
3. [Genral Error Resolution](#Genral-Error-Resolution)
4. [Contact](#contact)


## Spinnaker Setup
To set up Spinnaker on your system, follow these steps:

1. Copy the "testbed" folder to your desired directory.
2. Navigate to the "testbed" folder.
3. Provide execute permissions to two bash files by running the following commands sequentially:
   
    ```
    chmod +x setup_so.bash
    chmod +x setup_wheel.bash
    ```

4. Run the setup_so.bash file with superuser privileges:

    ```
    sudo ./setup_so.bash
    ```

5.	Follow all the prompt as follows:
        
    * Would you like to continue and install all the Spinnaker SDK packages?: Y
    * Read the terms and conditions if you want, and don’t forget to accept     
        the EULA license terms if you want to install 😊 or you can close the instructions right away and have a good sleep.
    * Use Keyboard to accept the terms.
    * Would you like to add a udev entry to allow access to USB hardware? Y
        
        Essential to accept as we will be accessing the camera without the admin rights.
    * To add a new member please enter username (or hit Enter to continue): 
        * Username: jetson
        * Adding user jetson to group flirimaging group. Is this OK? [Y/n]: `y`
        * On another prompt for adding user hit Enter

    * Do you want to restart the udev daemon?[Y/n]: `y`
    * Would you like to set USB-FS memory size to 1000 MB at startup (via /etc/rc.local)?

        By default, Linux systems only allocate 16 MB of USB-FS buffer memory for all USB devices.

        This may result in image acquisition issues from high-resolution cameras 
        or multiple-camera set ups.

        NOTE: You can set this at any time by following the USB notes in the included README. 
        [Y/n]: `y`

    * Would you like to have Spinnaker prebuilt examples available in your system path?

        This allows Spinnaker prebuilt examples to run from any paths on the system.

        NOTE: You can add the Spinnaker example paths at any time by following the "RUNNING PREBUILT UTILITIES"

        section in the included README.
        [Y/n]: `y`

    * Would you like to have the FLIR GenTL Producer added to GENICAM_GENTL64_PATH?
        This allows GenTL consumer applications to load the FLIR GenTL Producer.
        NOTE: You can add the FLIR producer to GENICAM_GENTL64_PATH at any time by following the GenTL Setup notes in the included README.[Y/n]: `y`

    * Don’t participate in feedback program, i.e, answer such prompt: `n`
    * This should be done now.
    * Now Reboot the Jetson Nano by executing the following command: 
        ```
        sudo reboot
        ```

This will set up Spinnaker on your system.


## PySpin Setup
To set up PySpin on your system, follow these steps:

1. After rebooting the Jetson Nano, return to the "testbed" folder.
2. Execute the following command.
    ```
    sudo ./setup_wheel.bash
    ```
This will set up PySpin on your system.

## Genral Error Resolution
1. The illegal instruction error can be solved using the command 
    ```
    export OPENBLAS_CORETYPE=ARMV8
    ```
2. If the code runs and doesn't detect your camera, try hooking it up to another USB port and run the file again.

## Contact
In case of any issues contact the following:
- Vishwesh Vhavle (vishwesh20156@iiitd.ac.in)
- Jatin Sharma (jatin20563@iiitd.ac.in)
