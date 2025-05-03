#!/bin/bash 

USER_DIR=''


if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    USER_DIR=$1 
fi 


cd ./env_docker

./setup_user_dir.sh $USER_DIR
./setup_volume.sh /home/

cd ..

sudo docker compose --env-file ./env_docker/docker_volume.env  up 
