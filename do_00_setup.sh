#!/usr/bin/bash

# pip install requirements-parser

../flatpak-builder-tools/pip/flatpak-pip-generator --runtime='org.freedesktop.Sdk//23.08' --requirements-file='virtualenv/requirements.x86_64.txt' --ignore-installed=portaudio,PyAudio --ignore-errors --output requirements

