FROM python:3.10-slim 

WORKDIR /app
COPY llm.py stt.py review.py  /app 


COPY requirements.flatpak.txt /app 

COPY questions.txt /app

RUN apt update
RUN apt upgrade -y
RUN apt install -y pulseaudio python3-pip python3-dotenv python3-pyaudio python3-gst-1.0  portaudio19-dev gstreamer1.0-pulseaudio python3-espeak python3-mesonpy libcairo2-dev libgirepository1.0-dev libsqlite3-dev libghc-setenv-dev  

#RUN ["/usr/bin/python3", "-m", "ensurepip"]


#RUN python3.10 -m venv /root/.virtualenvs/pillm310 --prompt pillm310 

#RUN . /root/.virtualenvs/pillm310/bin/activate

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN . /app/venv/bin/activate

RUN ["/app/venv/bin/python3", "-m", "pip","install", "--upgrade", "pip"]

RUN ["/app/venv/bin/python3", "-m", "pip" , "install" , "--break-system-packages" , "--no-cache-dir" , "-r" , "/app/requirements.flatpak.txt"]
#EXPOSE 80 

RUN ["/app/venv/bin/python3", "-m", "pip" , "install" , "--break-system-packages" , "--no-cache-dir" , "PyGObject==3.50.0"]


#CMD tail -f /dev/null ## do something forever

CMD  /app/venv/bin/python3 /app/llm.py --user_dir  ${ENV_USER_DIR}


