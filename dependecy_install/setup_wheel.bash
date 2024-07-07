ROOT=$PWD
echo "PySpin Setup is in process in $ROOT directory\n"

cd $ROOT/spinaker/

echo "Updaating the installed repositories and installing required ones."
sudo apt-get update
sudo apt-get install python-pip python3-pip
python3.6 -m pip install --upgrade numpy matplotlib==3.2.2 pillow dt_apriltags

echo "Installing the wheel file."
cd $ROOT/spinaker/wheel
echo $PWD
sudo python3.6 -m pip install spinnaker_python-2.6.0.160-cp36-cp36m-linux_aarch64.whl

echo "PySpin wheel file installation succesful.\nExiting the process."
cd $ROOT
