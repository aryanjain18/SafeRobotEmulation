ROOT=$PWD
echo "Setup is in process in $ROOT directory\n"

cd $ROOT/spinaker/

echo "Updaating the installed repositories and installing required ones."
sudo apt-get update
sudo apt-get install libusb-1.0-0
sudo apt-get install build-essential

echo "Startinng spinnaker process"
cd $ROOT/spinaker/spinnaker-2.6.0.160-arm64

sudo sh install_spinnaker_arm.sh 

echo "Installling wheel file to access spinnaker using python"

echo "Installation succesful.\nExiting the process."
cd $ROOT
echo "Rebooting after this process is crucial to make the changes in effect.\nMake sure to reboot the system"
echo "\n:)"
