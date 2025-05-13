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

Hostip="$(ip -4 -o a | awk '{print $4}' | cut -d/ -f1 | grep -v 127.0.0.1 | head -n1)"
echo $Hostip

#ENV_IP=$Hostip

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
./setup_pulse_server.sh tcp:${Hostip}:4713

cd ..

cp virtualenv/requirements.flatpak.txt src/.

cp files/pulseaudio.client.conf src/.
cp files/pulseaudio.default.pa src/. 
cp files/pulseaudio.daemon.conf src/.

sudo cp files/*.client.conf /etc/pulse/client.conf.d/.
#sudo cp files/*.default.pa /etc/pulse/default.pa.d/.
sudo cp files/*.daemon.conf /etc/pulse/daemon.conf


pactl load-module module-native-protocol-tcp auth-ip-acl=tcp:$Hostip:4713
#echo "module-waveout"
#pactl load-module module-waveout sink_name=output source_name=input record=0
#echo "module-native-protocol-tcp"
#pactl load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1

export USER_DIR 
export UID 
export GROUP
export USER_PWD
export Hostip

#sudo  docker compose --env-file ./env_docker/docker_volume.env --env-file ./env_docker/docker_pulse_server.env -f compose-win.yaml  --env ENV_USER_DIR=$USER_DIR --env ENV_UID=$UID --env ENV_GID=$GROUP --env ENV_PWD=$USER_PWD --env ENV_IP=$Hostip up 

sudo ENV_USER_DIR=$USER_DIR ENV_UID=$UID ENV_GID=$GROUP ENV_PWD=$USER_PWD ENV_IP=$Hostip docker compose --env-file ./env_docker/docker_volume.env --env-file ./env_docker/docker_pulse_server.env -f compose-win.yaml up   

#Containerip="$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' pi-llm)"
#echo $Containerip
#sudo ENV_USER_DIR=$USER_DIR ENV_UID=$UID docker compose --env-file ./env_docker/docker_volume.env exec pi-llm bash

echo 'run "docker compose down" to stop'
