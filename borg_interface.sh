#!/bin/bash

# Get the current working directory
SCRIPTPATH=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")

# add the bin directory to the path
PATH=$PATH:$SCRIPTPATH/borg_interface/bin/

# activate the virtual environment
source $SCRIPTPATH/borg_interface/bin/activate

# execute the main script
python3 $SCRIPTPATH/borg_interface/main.py
exit 0
