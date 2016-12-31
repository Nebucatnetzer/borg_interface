#!/bin/bash
INTERFACE_PATH=/home/andreas/.virtualenvs/borg_interface
PATH=$PATH:$INTERFACE_PATH/bin/
source $INTERFACE_PATH/bin/activate
python3 $INTERFACE_PATH/backup_to_external.py
exit 0
