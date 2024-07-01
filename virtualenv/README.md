# VIRTUALENV

Source the file named `do_make_virtualenv_setup310.sh` .

```
. ./do_make_virtualenv_setup310.sh 
```

# Requirements

After sourcing the above file, run this command to install dependencies.

```
./do_install_apt_pkg.sh
## This is for ubuntu or debian... ##

pip3 install -r ./requirements.not-flatpak.txt 
## Exit this folder and use repository normally... ##
```
