FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get  install -y

RUN apt-get -y install vim
RUN apt-get -y install python-pip
RUN apt-get -y install python-dev
RUN apt-get -y install swig
RUN apt-get -y install libboost-python-dev
RUN apt-get -y install libpulse-dev
RUN apt-get -y install libasound2-dev
RUN pip install pocketsphinx webrtcvad
RUN apt-get -y install portaudio19-dev
RUN apt-get -y install python-pyaudio
RUN apt-get -y install libasound-dev
RUN pip install pyaudio respeaker --upgrade
RUN pip install --pre pyusb
RUN pip install numpy
RUN mkdir ~/git
RUN cd ~/git
RUN apt-get -y install git
RUN git clone https://github.com/respeaker/seeed-voicecard.git
RUN git clone https://github.com/respeaker/mic_array.git
RUN cd seeed-voicecard && ./install.sh
#RUN reboot