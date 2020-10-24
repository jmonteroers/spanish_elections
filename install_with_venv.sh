#!/bin/bash

### Example usage ###
# your current directory pointing to the root of this repo...
# install in editor mode
# bash install_with_venv.sh venv . spanish_elections
# $1: name of virtual environment or absolute path to it
# $2: location of spanish_elections package
# $3: name of kernel with new virtual environment in jupyter notebook
# $4: whether to install in editor mode (default, leave empty)


python3 -m venv $1
source "$1/bin/activate"
# default is
if [ -z "$4" ]
  then
  python3 -m pip install -e $2
else
  python3 -m pip install $2
fi
# install jupyter
python3 -m pip install jupyter
ipython kernel install --name $3 --user
deactivate
