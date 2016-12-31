#!/bin/bash
SCRIPTPATH=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
PATH=$PATH:$SCRIPTPATH/bin/
source $SCRIPTPATH/borg_interface/bin/activate
python3 $SCRIPTPATH/borg_interface/backup_to_external.py
exit 0
