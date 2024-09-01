#!/bin/bash 

echo "go to this site and download GoogleNews-vectors-negative300.bin.gz"

echo 

echo "Put the file in a location beside the pi-llm project. Unzip it with"
echo "the command:"
echo "gunzip GoogleNews-vectors-negative300.bin.gz"
echo "You will have left the file GoogleNews-vectors-negative300.bin"

read  -n 1 -p "Continue to site:" xinput 

echo $xinput

xdg-open https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?resourcekey=0-wjGZdNAUop6WykTtMip30g
