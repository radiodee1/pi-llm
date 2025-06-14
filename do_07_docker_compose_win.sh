#! /usr/bin/env bash

echo $HOME
echo $UID
echo $(id -u)

#exit

#do_06_docker_compose_linux.sh
#!/bin/bash 

#sudo apt install net-tools -y

USER_DIR=$HOME
USER_PWD=$PWD 
echo $UID
echo $USER_DIR
GROUP=$(id -g)
echo $GROUP
echo $USER_PWD 
USER=$(whoami)
echo $USER

#net localgroup docker-users $USER /ADD

HOSTIP="$(ip -4 -o a | awk '{print $4}' | cut -d/ -f1 | grep -v 127.0.0.1 | head -n1)"
echo $HOSTIP

#ENV_IP=$Hostip

if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    USER_DIR=$1 
fi 

echo $USER_DIR

cd ./env_docker

echo "" > docker_pairs.env ## empty
echo "" > ../pulseaudio-win.env ## empty

./setup_user_dir.sh $USER_DIR
./setup_volume.sh $USER_DIR
./setup_pulse_server.sh unix:/mnt/wslg/PulseServer

cat docker*.env >> ../pulseaudio-win.env 

cd ..

sudo cp files/*.client.conf /etc/pulse/client.conf.d/.
sudo cp files/*.default.pa /etc/pulse/default.pa.d/.
sudo cat files/*.daemon.conf >> /etc/pulse/daemon.conf


ENV_VOLUME=$USER_DIR ENV_USER_DIR=$USER_DIR ENV_UID=$UID ENV_GID=$GROUP ENV_IP=$HOSTIP ENV_PULSE_SERVER=unix:/mnt/wslg/PulseServer docker compose -f compose-win.yaml --env-file ./pulseaudio-win.env up -d 


echo 'type "exit" below to get terminal back'

ENV_VOLUME=$USER_DIR ENV_USER_DIR=$USER_DIR ENV_UID=$UID ENV_GID=$GROUP ENV_IP=$HOSTIP ENV_PULSE_SERVER=unix:/mnt/wslg/PulseServer docker run -it -v $USER_DIR:$USER_DIR -v /var/run/user/${UID}/:/var/run/user/${UID}/ -v /mnt/wslg/PulseServer:/mnt/wslg/PulseServer pi-llm-pi-llm  bash    

echo 'run "docker compose down" to stop'
