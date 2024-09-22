#!/bin/bash 

echo "Go to this site and download GoogleNews-vectors-negative300.bin.gz"

echo 

echo "Put the file in a location beside the pi-llm project. Unzip it with"
echo "the command:"
echo ""
echo "gunzip GoogleNews-vectors-negative300.bin.gz"
echo ""
echo "You will have left the file GoogleNews-vectors-negative300.bin"
echo ""
read  -n 1 -p "Continue to site/Break(Ctl-c):" xinput 

echo $xinput

xdg-open https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?resourcekey=0-wjGZdNAUop6WykTtMip30g
