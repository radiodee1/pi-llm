#!/usr/bin/env bash 


HOST_FILE='docker_user_dir.env'

USER_DIR=''


if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    USER_DIR=$1 
fi 


echo "# env" > $HOST_FILE
echo "ENV_USER_DIR=${USER_DIR}" >> $HOST_FILE
echo "# empty?? " >> $HOST_FILE

