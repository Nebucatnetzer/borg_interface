#!/bin/bash
SCRIPTPATH=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
PATH=$PATH:$SCRIPTPATH/bin/
source $SCRIPTPATH/bin/activate
python3 $SCRIPTPATH/backup_to_external.py
exit 0
