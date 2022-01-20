FROM jupyter/scipy-notebook:latest

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir notebook

RUN pip install --no-cache-dir music21==7.1.0

#RUN apt install software-properties-common
#RUN apt-get update
#RUN add-apt-repository ppa:mscore-ubuntu/mscore3-stable
#RUN apt-get update
RUN apt install musescore3

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
    
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


