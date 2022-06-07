# pyaudioのサポートがpython3.6までなので
FROM python:3.6
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN sudo apt-get update
RUN sudo apt-get upgrade
RUN sudo apt-get -y install vim
RUN sudo apt-get -y install swig
RUN sudo apt-get -y install libboost-python-dev
RUN sudo apt-get -y install libpulse-dev
RUN pip install pocketsphinx webrtcvad
RUN sudo apt-get -y install python-pyaudio
RUN sudo apt-get -y install libasound-dev
RUN sudo pip install pyaudio respeaker --upgrade
RUN sudo apt-get -y install portaudio19-dev
RUN sudo pip install --pre pyusb
RUN sudo pip install numpy
RUN mkdir ~/git
RUN cd ~/git
RUN sudo apt-get -y install git
RUN git clone https://github.com/respeaker/seeed-voicecard.git
RUN git clone https://github.com/respeaker/mic_array.git
RUN cd seeed-voicecard
RUN sudo ./install.sh 4mic