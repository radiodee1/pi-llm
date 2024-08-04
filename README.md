# pi-llm
containerized llm for raspberry pi

## Setup and Build

- Go to the `virtualenv` folder and execute the `do_install_apt_pkg.sh` file. If you are not on a ubuntu distro you will need to  go through the `do_install_apt_pkg.sh` file and install the packages on your system that are necessary.
- Make sure that you have python 3.10 installed. You may need to build python from source.
- `source` the `do_make_virtualenv_setup310.sh` file. You will want to do this any time you want to run the program outside of the containerized setup. After sourcing the file return to the `pi-llm` root directory. You should actually be able to run the scripts without containerization now. If you want to run the word counting script or the plotting script, this is important.

## Flatpak scripts

- `do_00_setup.sh` - runs setup script, which is 'flatpak-builder-tools'. This assumes that you git clone the flatpak-builder-tools repo in the directory next to pi-llm. Since the pi-llm project includes a requirements.json file, this is probably not necessary for every user.
- `do_01_build.sh` - runs the flatpak command that builds the flatpak for `x86_64`. The program, flatpak-builder, needs to have been installed already.
- `do_02_try.sh` - runs the flatpak in the `x86_64` environment. 
- `do_03_aarch64.sh` - build a flatpak package for `aarch64`.
- `do_04_stom.sh` - stop the flatpak in the `x86_64` environment.

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

Below are some test arguments for the `PROJECT_LAUNCH_ARGS` variable. If the `PROJECT_LAUNCH_ARGS` variable is not empty, the program will launch using the variable contents only. In other words if the variable is set the program will no longer parse command line arguments, and will parse the `PROJECT_LAUNCH_ARGS` instead. This is so that the program can launch with different configurations from run to run when containerized in a flatpak.

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

