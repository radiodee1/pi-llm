#!/usr/bin/bash
flatpak install flathub org.gnome.Sdk/aarch64/48 -y 
flatpak install flathub org.freedesktop.Platform/aarch64/24.08 -y
flatpak install flathub org.freedesktop.Sdk/aarch64/24.08 -y 
flatpak install flathub org.gnome.Platform/aarch64/48 -y

flatpak-builder --user --arch=aarch64 --disable-tests --repo=repo build-dir org.llm.LLM.yaml --force-clean 

flatpak build-bundle --arch=aarch64 ./repo org.llm.LLM.aarch64.flatpak org.llm.LLM
