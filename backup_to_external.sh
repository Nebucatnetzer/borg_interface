#!/bin/bash
PATH=$PATH:borg_interface/bin/
source borg_interface/bin/activate
python3 borg_interface/backup_to_external.py
exit 0
