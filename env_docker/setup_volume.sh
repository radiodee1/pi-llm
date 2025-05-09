#!/usr/bin/env bash 


HOST_FILE='docker_volume.env'

VOLUME=''


if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    VOLUME=$1 
fi 


echo "# env" > $HOST_FILE
echo "ENV_VOLUME=${VOLUME}" >> $HOST_FILE
echo "# empty?? " >> $HOST_FILE

