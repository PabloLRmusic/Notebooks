FROM jupyter/scipy-notebook
RUN pip install music21
USER root
RUN apt-get update; \
    apt-get install -y software-properties-common; \
    add-apt-repository ppa:mscore-ubuntu/mscore3-stable; \
    apt-get update; \
    apt-get install -y musescore3; \
    rm -rf /var/lib/apt/lists/*
USER jovyan
ENV QT_QPA_PLATFORM=offscreen
RUN python -c "from music21 import * ; us = environment.UserSettings(); \
us['musescoreDirectPNGPath'] = '/home/jovyan'; \ 
us['pdfPath'] = '/usr/bin/musescore3'; \
us['graphicsPath'] = '/usr/bin/musescore3'; \
us['musescoreDirectPNGPath'] = '/usr/bin/musescore3'; \
us['musicxmlPath'] = '/usr/bin/musescore3';"
