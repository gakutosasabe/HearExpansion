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

# Vim使えないけど練習のため
RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# 一応Jupyternotebookも入れておく
RUN python -m pip install jupyterlab

# pyaudioはPortaudioに依存しているため
RUN apt-get install portaudio19-dev 

# pyaudioのインストール
RUN pip install pyaudio

# Speech recognitionのインストール
RUN pip install SpeechRecognition

# pycawのインストール
RUN pip install pycaw

