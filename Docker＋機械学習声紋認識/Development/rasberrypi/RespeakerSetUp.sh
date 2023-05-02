sudo apt-get update
sudo apt-get  install -y

sudo apt-get -y install vim
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev
sudo apt-get -y install swig
sudo apt-get -y install libboost-python-dev
sudo apt-get -y install libpulse-dev
sudo apt-get -y install libasound2-dev
sudo pip install pocketsphinx webrtcvad
sudo apt-get -y install portaudio19-dev
sudo apt-get -y install python-pyaudio
sudo apt-get -y install libasound-dev
sudo pip install pyaudio respeaker --upgrade
sudo pip install --pre pyusb
sudo pip install numpy
sudo mkdir ~/git
sudo cd ~/git
sudo apt-get -y install git
sudo git clone https://github.com/respeaker/seeed-voicecard.git
sudo git clone https://github.com/respeaker/mic_array.git
sudo cd seeed-voicecard && ./install.sh 4mic
sudo reboot
