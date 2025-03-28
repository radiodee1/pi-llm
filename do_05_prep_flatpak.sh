#!/usr/bin/bash

flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo --user

flatpak install flathub org.gnome.Sdk//48 -y --user
flatpak install flathub org.freedesktop.Platform//24.08 -y --user 
flatpak install flathub org.freedesktop.Sdk//24.08 -y --user 
flatpak install flathub org.gnome.Platform//48 -y --user



