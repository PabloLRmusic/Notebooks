FROM jupyter/scipy-notebook:latest

RUN pip install music21

USER root
RUN apt-get install -y software-properties-common; \
    yes | add-apt-repository ppa:mscore-ubuntu/mscore3-stable; \
    apt-get update; \
    apt-get install musescore3; \
   
RUN python -c "from music21 import *; us = environment.UserSettings(); environment.set('pdfPath', '/usr/bin/musescore3'); environment.set('graphicsPath', '/usr/bin/musescore3'); environment.set('musescoreDirectPNGPath', '/usr/bin/musescore3'); environment.set('musicxmlPath', '/usr/bin/musescore3');"
