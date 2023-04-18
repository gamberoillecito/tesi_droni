# comandi presi da https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html
#sudo usermod -a -G dialout $USER
#sudo apt-get remove modemmanager -y
#sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
#sudo apt install libqt5gui5 -y
#sudo apt install libfuse2 -y

wget https://d176tv9ibo4jno.cloudfront.net/latest/QGroundControl.AppImage
chmod +x ./QGroundControl.AppImage
# questo comando e' suggerito da questo commento (solo per installazione tramite WSL2)
# https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html
#sudo apt-get install -y libpulse-dev
