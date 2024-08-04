# pi-llm
containerized llm for raspberry pi

## Env File

Put key values in a file called `~/.llm.env`. An example follows.

```bash
# Test values...
TEST_SIX=6
TEST_NINE=9

OPENAI_API_KEY=abc
# OPENAI_MODEL=abc

GOOGLE_SPEECH_RECOGNITION_API_KEY=abc

MICROPHONE_INDEX=-1
PROJECT_LAUNCH_ARGS=''

# For Google Cloud Speech...
GOOGLE_APPLICATION_CREDENTIALS=/path-to-json-file/file.json

```
## Launch Args 

Below are some test arguments for the PROJECT_LAUNCH_ARGS variable. If the `PROJECT_LAUNCH_ARGS` variable is not empty, the program will launch usint the variable contents only. If the variable is set the program will no longer parse command line arguments, and will parse the `PROJECT_LAUNCH_ARGS` instead. This is so that the program can launch with different configurations from run to run when containerized in a flatpak.

```
PROJECT_LAUNCH_ARGS='--file --loop_wait --verbose --name Bob --offset 20 --timeout 0.5 --cloud'
```

- Collision checking does not work well. Do not use `--check`. 

- Cloud speech recognition, `--cloud`, works well but is largely untested. You must install a json file on the host computer and provide a path to that file in the `GOOGLE_APPLICATION_CREDENTIALS` variable. This file is provided by Google when you set up your Google cloud account. You must also enable billing and 'Cloud Speech to Text'. Do not share this file or path with anyone.

- Remember that background noise is allways a problem. The microphone will hang if there's too much background noise and the end of input text will not be detected.

- If you leave the `OPENAI_MODEL` unset, the default will be used, which is "gpt-3.5-turbo".

## Autostart

- Make a folder on the raspberry pi if one doesn't exist.
```
mkdir ~/.config/autostart 
```
- In the folder make a desktop launcher file that launches your flatpak. The name needs the `.desktop` extension. (for example 'myapp.desktop')
```
[Desktop Entry]
Type=Application
Name=Pi LLM 
Exec=/usr/bin/flatpak run --branch=master --arch=aarch64 --devel --user --command=/app/bin/llm.py org.llm.LLM 
Comment=Containeriized LLM for raspberry pi 
```

