#!/usr/bin/bash
flatpak install flathub org.gnome.Sdk//48 --user -y 
flatpak install flathub org.freedesktop.Platform//24.08 --user -y
flatpak install flathub org.freedesktop.Sdk//24.08 --user -y 
flatpak install flathub org.gnome.Platform//48 --user -y

flatpak-builder --user --install build-dir org.llm.LLM.yaml --force-clean 


