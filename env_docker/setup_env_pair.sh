#!/usr/bin/env bash 


HOST_FILE='docker_pairs.env'

VOLUME=''


if [ $# -ne '2' ]; then
    echo "NAME VALUE pairs"
else
    NAME=$1
    VALUE=$2 
fi 


echo "${NAME}=${VALUE}" >> $HOST_FILE

