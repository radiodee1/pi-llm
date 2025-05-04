#FROM ubuntu:24.10 AS builder 
FROM python:3.10-slim 
#ENV VITE_HOST=host.docker.internal

WORKDIR /app
COPY llm.py stt.py review.py  /app 


COPY requirements.flatpak.txt /app 

RUN apt update
RUN apt upgrade -y
RUN apt install -y pulseaudio python3-pip python3-dotenv python3-pyaudio python3-gst-1.0  portaudio19-dev python3-espeak python3-mesonpy libcairo2-dev libgirepository1.0-dev libsqlite3-dev libghc-setenv-dev  

RUN ["/usr/bin/python3", "-m", "pip" , "install" , "--break-system-packages" , "--no-cache-dir" , "-r" , "/app/requirements.flatpak.txt"]
#EXPOSE 80 

RUN ["/usr/bin/python3", "-m", "pip" , "install" , "--break-system-packages" , "--no-cache-dir" , "PyGObject==3.50.0" ]

CMD echo ${ENV_USER_DIR}

CMD  /usr/bin/python3 /app/llm.py --user_dir  ${ENV_USER_DIR}

#RUN apt install -y mpg123
#COPY *.mp3 /app 

#CMD /usr/bin/mpg123 /app/output.mp3 
