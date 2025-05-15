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

#Hostip="$(ip -4 -o a | awk '{print $4}' | cut -d/ -f1 | grep -v 127.0.0.1 | head -n1)"
#echo $Hostip

#ENV_IP=$Hostip

if [ $# -ne '1' ]; then
    echo ""
    echo "Enter a USER_DIR or leave blank for this user."
    echo "Enter empty double quotation marks for 'none'."
else
    USER_DIR=$1 
fi 


cd ./env_docker

echo "" > docker_pairs.env ## empty
echo "" > ../pulseaudio-win.env ## empty

./setup_user_dir.sh $USER_DIR
./setup_volume.sh $USER_DIR
#./setup_pulse_server.sh tcp:${Hostip}:4713
./setup_pulse_server.sh unix:/mnt/wslg/PulseServer
#/var/run/user/$UID/pulse/native

#./setup_env_pair.sh ENV_VOLUME $USER_DIR

cat docker*.env >> ../pulseaudio-win.env 

cd ..

cp virtualenv/requirements.flatpak.txt src/.

cp files/pulseaudio.client.conf src/.
cp files/pulseaudio.default.pa src/. 
cp files/pulseaudio.daemon.conf src/.


sudo cp files/*.client.conf /etc/pulse/client.conf.d/.
sudo cp files/*.default.pa /etc/pulse/default.pa.d/.
sudo cp files/*.daemon.conf /etc/pulse/daemon.conf

#pactl load-module module-native-protocol-unix  socket=/mnt/wslg/PulseServer

#pactl load-module module-native-protocol-tcp   auth-ip-acl=tcp:0.0.0.0:4713
#echo "module-waveout"
#pactl load-module module-waveout sink_name=output source_name=input record=0
#echo "module-native-protocol-tcp"
#pactl load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1

#sudo chown -R 0 $USER_DIR
chmod -R 777 $USER_DIR

sudo ENV_VOLUME=$USER_DIR ENV_USER_DIR=$USER_DIR ENV_UID=$UID ENV_GID=$GROUP  ENV_IP=$Hostip ENV_PULSE_SERVER=unix:/mnt/wslg/PulseServer docker compose -f compose-win.yaml --env-file ./pulseaudio-win.env up   



#sudo  ENV_VOLUME=$USER_DIR ENV_USER_DIR=$USER_DIR ENV_UID=$UID ENV_GID=$GROUP ENV_PWD=$USER_PWD ENV_IP=$Hostip docker compose --env-file ./pulseaudio-win.env -f compose-win.yaml up   

#Containerip="$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' pi-llm)"
#echo $Containerip
#sudo ENV_USER_DIR=$USER_DIR ENV_UID=$UID docker compose --env-file ./env_docker/docker_volume.env exec pi-llm bash

echo 'run "docker compose down" to stop'
