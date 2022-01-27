FROM jupyter/scipy-notebook
RUN pip install music21
USER ROOT
RUN apt-get update; \
    apt-get install -y software-properties-common; \
    add-apt-repository ppa:mscore-ubuntu/mscore3-stable; \
    apt-get update; \
    apt-get install -y musescore3
    
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
ENV QT_QPA_PLATFORM=offscreen
RUN python -c "from music21 import *; us = environment.UserSettings(); environment.set('pdfPath', '/usr/bin/musescore3'); environment.set('graphicsPath', '/usr/bin/musescore3'); environment.set('musescoreDirectPNGPath', '/usr/bin/musescore3'); environment.set('musicxmlPath', '/usr/bin/musescore3');"
