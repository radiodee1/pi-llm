#!/usr/bin/bash

# pip install requirements-parser

../flatpak-builder-tools/pip/flatpak-pip-generator --runtime='org.gnome.Sdk//43' --requirements-file='virtualenv/requirements.x86_64.txt' --ignore-installed=portaudio,PyAudio,pygobject --ignore-errors --output requirements

