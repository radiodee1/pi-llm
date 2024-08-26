#!/usr/bin/bash
flatpak install flathub org.gnome.Sdk/aarch64/45 -y 
flatpak install flathub org.freedesktop.Platform/aarch64/23.08 -y
flatpak install flathub org.freedesktop.Sdk/aarch64/23.08 -y 
flatpak install flathub org.gnome.Platform/aarch64/45 -y

flatpak-builder --user --arch=aarch64 --disable-tests --repo=repo build-dir org.llm.LLM.yaml --force-clean 

#flatpak-builder --repo=repo --force-clean build-dir org.llm.LLM.yaml

#flatpak-builder --install build-dir org.llm.LLM.yaml

flatpak build-bundle --arch=aarch64 ./repo org.llm.LLM.aarch64.flatpak org.llm.LLM
