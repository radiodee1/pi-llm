#! /usr/bin/env bash

echo $HOME
echo $UID
echo $(id -u)

#exit

#do_06_docker_compose_linux.sh
#!/bin/bash 

USER_DIR=$HOME 
USER_PWD=$PWD 
echo $UID
echo $USER_DIR
GROUP=$(id -g)
echo $GROUP
echo $USER_PWD 

if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    USER_DIR=$1 
fi 


cd ./env_docker

./setup_user_dir.sh $USER_DIR
./setup_volume.sh $USER_DIR

cd ..

cp virtualenv/requirements.flatpak.txt src/.

pactl load-module module-native-protocol-unix socket=/mnt/wslg/PulseServer

sudo ENV_USER_DIR=$USER_DIR ENV_UID=$UID ENV_GID=$GROUP ENV_PWD=$USER_PWD docker compose --env-file ./env_docker/docker_volume.env -f compose-win.yaml up   

#sudo ENV_USER_DIR=$USER_DIR ENV_UID=$UID docker compose --env-file ./env_docker/docker_volume.env exec pi-llm bash

echo 'run "docker compose down" to stop'
