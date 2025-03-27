#!/usr/bin/bash

flatpak install flathub org.gnome.Sdk//48 -y 
flatpak install flathub org.freedesktop.Platform//24.08 -y
flatpak install flathub org.freedesktop.Sdk//24.08 -y 
flatpak install flathub org.gnome.Platform//48 -y


../flatpak-builder-tools/pip/flatpak-pip-generator --runtime='org.gnome.Sdk//48' --requirements-file='virtualenv/requirements.flatpak.txt' --ignore-installed=setuptools,portaudio,PyAudio,pygobject --ignore-errors --output requirements ## --runtime='org.gnome.Sdk//45'

