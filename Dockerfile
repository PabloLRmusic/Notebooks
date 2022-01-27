FROM jupyter/scipy-notebook:latest

RUN pip install music21

USER root
RUN apt-get update; \
    apt-get install -y software-properties-common; \
    apt-utils; \
    add-apt-repository ppa:mscore-ubuntu/mscore-stable; \
    apt-get update; \
    apt-get install -y lilypond; \
    apt-get install -y musescore; \
    rm -rf /var/lib/apt/lists/*
ARG NB_USER=visitor
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
   
RUN python -c "from music21 import environment; us = environment.UserSettings(); us['musescoreDirectPNGPath'] = '/home/jovyan/work'; us['musicxmlPath'] = '/usr/bin/mscore'; us['lilypondPath'] = '/usr/bin/lilypond';"
