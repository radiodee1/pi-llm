#!/usr/bin/env bash 


HOST_FILE='docker_pulse_server.env'

PULSE=''


if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    PULSE=$1 
fi 


echo "# env" > $HOST_FILE
echo "PULSE_SERVER=${PULSE}" >> $HOST_FILE
echo "# empty?? " >> $HOST_FILE

