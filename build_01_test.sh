#!/usr/bin/bash
flatpak install flathub org.gnome.Sdk//43 -y 
flatpak install flathub org.freedesktop.Platform//23.08 -y
flatpak install flathub org.freedesktop.Sdk//23.08 -y 

sudo flatpak-builder --install build-dir org.llm.LLM.yaml --force-clean 

#flatpak-builder --repo=repo --force-clean build-dir org.llm.LLM.yaml

#flatpak-builder --install build-dir org.llm.LLM.yaml

