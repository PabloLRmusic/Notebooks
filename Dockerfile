FROM jupyter/scipy-notebook:latest

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1001 ubuntu
USER ubuntu
WORKDIR /home/ubuntu

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir notebook

RUN pip install --no-cache-dir music21==7.1.0

#RUN pip install --no-cache-dir jupyterhub

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:mscore-ubuntu/mscore3-stable

RUN apt install musescore3


