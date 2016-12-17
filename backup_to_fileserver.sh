#!/bin/bash
PATH=$PATH:borg_interface/bin/
source borg_interface/bin/activate
python3 borg_interface/backup_to_fileserver.py
exit 0
