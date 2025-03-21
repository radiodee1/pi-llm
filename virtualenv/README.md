# VIRTUALENV

## Requirements 

Install some necessary apt packages.
```
./do_install_apt_pkg.sh
## This is for ubuntu or debian... ##
```

Build the Python-3.10 source package as detailed below. Then source the file named `do_make_virtualenv_setup310.sh` .

```
. ./do_make_virtualenv_setup310.sh 
## This sets up the virtualenv for the project as a whole ##
```

After sourcing the above file, run this command to install dependencies.

```
pip3 install -r ./requirements.not-flatpak.txt 
## Exit this folder and use repository normally... ##
```

# Python 3.10 Install 

You must install all the dev components for sqlite3. At the time of this writing it is done with the package `libsqlite3-dev`. These instructions are for debian/ubuntu.

```
## remember the do_install_apt_pkg.sh script above ##

## move to some location on the system where you can work. ##
cd ~/workspace

## Download the source package. ##
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz

## Uncompress file ##
tar xvzf Python-3.10.14.tgz

## switch to Python directory ##
cd Python-3.10.14 

## configure with sqlite ##
./configure --enable-loadable-sqlite-extensions 

## make ##
make 

## install (very important to use 'altinstall') ##
sudo make altinstall
```
