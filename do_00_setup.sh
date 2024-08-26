#!/usr/bin/bash


../flatpak-builder-tools/pip/flatpak-pip-generator --runtime='org.gnome.Sdk//45' --requirements-file='virtualenv/requirements.x86_64.txt' --ignore-installed=setuptools,portaudio,PyAudio,pygobject --ignore-errors --output requirements ## --runtime='org.gnome.Sdk//45'

