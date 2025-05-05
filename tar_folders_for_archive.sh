#!/bin/bash 

cd ..

tar czf  pi-llm.tar.gz --exclude=".git" --exclude=".flatpak-builder" --exclude="__pycache__" --exclude="build-dir" --exclude="repo" --exclude="*.flatpak"  pi-llm 
