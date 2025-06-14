# pi-llm
Containerized llm for raspberry pi, and maybe other platforms.

What follows is a verbose set of notes put together from the start of the project.

## On-Line Services

- You need a Google cloud account and a json file on your hard drive containing Google's authorization code. Google will supply you with one of these when you setup your Google cloud account. You set up a project and an account to pay for it with, and then you enable all the services you require. The path to the json file is stored in the `~/.llm.env` file in the `GOOGLE_APPLICATION_CREDENTIALS` key.
- There is a Speech to Text feature in the code as a default, but Google Code is an option and it works better. For Speech To Text you must enable Google Cloud Speech To Text on the Google Cloud site for your project. To tell the code that you want Google STT, pass the program `--cloud_stt` as an option.
- There is a Text to Speech option in the code, but Google Code TTS is an option and it works better. For Google Text To Speech you must enable Google Cloud Text To Speech on the Google Cloud site for your project. To tell the code that you want Google TTS, pass the program `--cloud_tts` as a launch option.
- One essential part of the program queries an OpenAI model to determine what the program's next output will be. This is not an optional part of the program. You must have an OpenAI account and an OpenAI user key. This info goes into the `~/.llm.env` file. The key information is stored in the `OPENAI_API_KEY` variable.
- You can use Google gemini. You must go to the gemini web site and get a key and store it in the .llm.env file as GOOGLE_GEMINI_API_KEY. Then put the gemini model name that you are interested in in the GOOGLE_GEMINI_MODEL. Then pass `--google_gemini` as a launch argument. You must do all of this in addition to setting up the GOOGLE_APPLICATION_CREDENTIALS. See the google web site: https://aistudio.google.com/app/apikey 

## Setup 
It is possible to run the code from the project without containerization. This is essential for running the count and plot scripts.

- Go to the `virtualenv` folder and execute the `do_install_apt_pkg.sh` file. If you are not on a ubuntu distro you will need to  go through the `do_install_apt_pkg.sh` file and install the packages on your system that are necessary. The script may work on debian but it has not been tested.
- Make sure that you have python 3.10 installed. You may need to build python from source. This is important. You want to make sure that `sqlite3` is available when you run your scripts. This needs to be assured during the python build. Instructions for installing Python from scratch are included in the `README.md` file in the `virtualenv` directory.
- `source` the `do_make_virtualenv_setup310.sh` file. You will want to do this any time you want to run the program outside of the containerized setup. After sourcing the file return to the `pi-llm` root directory. 
- Execute the command `pip install -r virtualenv/requirements.not-flatpak.txt`. This will ssetup all the python packages in the python virtual environment. You should have to do this once succsessfully. After that the packages will be available any time you enter the python environment.
- You should actually be able to run the scripts without containerization now. If you want to run the word counting script or the plotting script, this is important.

## Flatpak scripts

- `do_00_setup.sh` - runs setup script, which is 'flatpak-builder-tools'. This assumes that you git clone the flatpak-builder-tools repo in the directory next to pi-llm. Since the pi-llm project includes a requirements.json file, this is probably not necessary for every user.
- `do_01_build.sh` - runs the flatpak command that builds the flatpak for `x86_64`. The program, flatpak-builder, needs to have been installed already.
- `do_02_try.sh` - runs the flatpak in the `x86_64` environment. 
- `do_03_aarch64.sh` - build a flatpak package for `aarch64`.
- `do_04_stop.sh` - stop the flatpak that may or may not be running in the `x86_64` environment.
- `do_05_prep_flatpak.sh` - Often when you go to a new architecture it is necessary to install some base flatpak packages. This script is suposed to make installing base flatpak packages more easy.

## Env File

Put key values in a file called `~/.llm.env`. An example follows.

```bash
OPENAI_API_KEY=abc
# OPENAI_MODEL=abc

MICROPHONE_INDEX=-1
PROJECT_LAUNCH_ARGS=''

# For Google Cloud Speech...
GOOGLE_APPLICATION_CREDENTIALS=/path-to-json-file/file.json

OPENAI_CHECKPOINTS="abc,abc,abc"

GOOGLE_GEMINI_URL="https://generativelanguage.googleapis.com/v1beta/models/"

GOOGLE_GEMINI_API_KEY="" ## get this from google web site...
## https://aistudio.google.com/app/apikey 

GOOGLE_GEMINI_MODEL="gemini-2.0-flash"

```
Google gemini usage works. The GOOGLE_GEMINI key/value pairs work but you don't need them if you use OpenAI. For now they don't do anything unless you pass the flag `--google_gemini` in the Env file. Get your own GOOGLE_GEMINI_API_KEY from the google web site: https://aistudio.google.com/app/apikey 


## Launch Args 

Below are some test arguments for the `PROJECT_LAUNCH_ARGS` variable. If the `PROJECT_LAUNCH_ARGS` variable is not empty, the program will launch using the variable contents only. In other words if the variable is set the program will no longer parse command line arguments, and will parse the `PROJECT_LAUNCH_ARGS` instead. This is so that the program can launch with different configurations from run to run when containerized in a flatpak.

```
PROJECT_LAUNCH_ARGS='--file --verbose --name Bob --offset 20 --timeout 0.5 --cloud_stt --cloud_tts --voice male '
```

- Collision checking does not work well. Do not use `--check`. 
- Cloud speech recognition, `--cloud_stt`, works well but is largely untested. You must install a json file on the host computer and provide a path to that file in the `GOOGLE_APPLICATION_CREDENTIALS` variable. This file is provided by Google when you set up your Google cloud account. You must also enable billing and 'Cloud Speech to Text'. Do not share this file or path with anyone.
- Cloud speech generation is available from Google as well. To use this feature include the `--cloud_tts` flag. You must enable 'Cloud Text to Speech' on the Google site and assure that billing is attached to your Google account and project.
- Remember that background noise is allways a problem. The microphone will hang if there's too much background noise and the end of input text will not be detected.
- If you leave the `OPENAI_MODEL` unset, the default will be used, which is "gpt-3.5-turbo".
- You can choose a male or female voice using the `--voice` flag.
- You can use the `--questions` flag as noted below.
- Do not use `--loop_wait` if you are using the `--cloud_stt` flag.

## `--questions` Flag 

There is a `--questions` flag. It takes one argument. It is used in the `PROJECT_LAUNCH_ARGS` environment variable. This option uses the `OPENAI_CHECKPOINTS` model list from the environments file. This list is composed of comma separated names of model checkpoints. The program goes through the checkpoints one at a time querying them with the contents of the `questions.txt` list. The checkpoints must already exist. You should finetune an OpenAI model in order to test the checkpoints with this option.

You use the `--questions` flag to simulate a two person (bot) conversation. You pass the flag and also the number of exchanges between the bot and it's counterpart. This would look like `--questions 20` where '--questions' is the flag on the PROJECT_LAUNCH_ARGS line and '20' is how many exchanges you want. There is a file in the `src` folder of the repository that contains the project source code, but also the file with the preset `--questions` text. You can change these presets before building the flatpak. There are basically two extremes for this file. The long option requires that you make up many fact-based questions. The short option requires that you make up fewer questions but some of the questions are not simple factual answers.


The longer version:
```
## There may be as many as 40 sentences in this file.
What is your name?
How old are you?
...
```

The shorter version:
```
## There may be only a few examples in this file.
Say something inspirational about how to spend your time wiseley.
```

The two `questions.txt` files produce slightly different results. The `--questions` flag must specify a number equal to or greater than the number of lines in the `questions.txt` file. Though the examples on this page use comments, no actual comment lines are allowed in the `questions.txt` file.

Again, this option goes through the checkpoints in the `OPENAI_CHECKPOINTS` environment variable and uses the `questions.txt` file to query the model. Resulting output is saved to the `/home/<name>` folder as different files for each checkpoint. You can then use the `count.py` and `plot.py` scripts on the checkpoint file in batches.

The `--questions` flag may not work on the docker images.

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

## Resetting `--user_dir`

- The `--user_dir` flag takes one argument. The argument is the new location for the `.llm.env` file and all output.
- You can set `--user_dir` at the command line (not in `.llm.env`). Then the program will look for the `.llm.env` file in the newly specified location. 
- Output to the new location is dependent on the permissions that the app has when it is run. If you do not set the `--user_dir` below the user's home dir, things like the `--file` output, which requires 'write' permission, may not work.
- You can also put the `--user_dir` argument in the `.llm.env` file, but your results may be unpredictable.
- `--user_dir` is not employed in the 'flatpak'.
- You should consider that the environment file has a variable that points to the GOOGLE_APPLICATION_CREDENTIALS location. If this is not readable the `--cloud_stt` option will fail. This might happen in a Docker-compose setting. If the code is meant to point to a Windows 'users' directory, the GOOGLE_APPLICATION_CREDENTIALS location should also be in that directory.

## Docker for Linux
This was tested on Debian 11 and Ubuntu 24.10. 
```
## Note: this code uses 'pulseaudio.'

sudo apt install -y pulseaudio pulseaudio-utils
cd ~
mkdir workspace
cd workspace
git clone https://github.com/radiodee1/pi-llm.git 
cd ~/workspace/pi-llm/
./do_06_docker_compose_linux.sh 
```
## Docker for Windows
This currently works only minimally. On a fresh install of Windows 10, install the following:
- WSL - Necessary for Docker. In PowerShell type: `wsl --install`
- pulseaudio - An installer package is called `pasetup.exe` from Patrick Gaskin at 'pgaskin.net'. Also you can install the package from WSL, and this is what I have been attempting. Maybe try `sudo apt install pulseaudio`.
- Git-for-windows
- Docker Desktop Installer.exe - available for users in small organizations that make less than a certain amount. Using `winget` to install Docker CLI did not work for me. Also, make sure to open Docker Desktop and go to "Settings" > "Resources" > "WSL Integration" and enable integration with your Linux distro (for me this was Ubuntu.)
- The size of the Windows install is important. If you use a VM, the size of the disk image should probably be larger than 80G.
```
## Start in the home directory using the WSL terminal.

sudo apt install pulseaudio

cd ~
mkdir workspace 
cd workspace
git clone https://github.com/radiodee1/pi-llm.git 
cd ~/workspace/pi-llm/

## You should type this in the WSL terminal!!
./do_07_docker_compose_win.sh

## You should be able to specify another WSL path for the pi-llm installation.
./do_07_docker_compose_win.sh /mnt/some/other/path 

## The above only works with Linux path names, 
## but need not be limited to the '/mnt' or '/home' directory.
```

If you specify your own install path, it will probably only work in the WSL name space. If you try to use Windows paths, the program will complain that the path that you supply contains too many colons. If you manage to call the script (`do_07_docker_compose_win.sh`) using colon free path names, you may be able to run the model. Note that the config file (`.llm.env`) has an entry for GOOGLE_APPLICATION_CREDENTIALS, and this entry contains a path to the Google json file. This should be considered and possibly adjusted.

## Notes

Here are some notes so I don't forget how to do things at the command line that I have not memorized.

```
sudo docker image rmi --force $(sudo docker images -a -q)

docker run -it pi-llm-pi-llm bash
```
