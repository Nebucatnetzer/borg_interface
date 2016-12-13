#!/usr/bin/env python3
import os
import sys
import configparser
import subprocess

chosen_activity = None
mount_point = None

# setup the config parser
config = configparser.ConfigParser()

# read config file
config.read('borg_interface.cfg')

# assign the repository variable
if 'server' in config:
    repository = (config['DEFAULT']['user']
                 + "@"
                 + config['DEFAULT']['server']
                 + ":"
                 + config['DEFAULT']['repository_path'])
else:
    repository = config['DEFAULT']['repository_path']

# assign the password variable
password = config['DEFAULT']['password']

# set the environment variables
os.environ['BORG_REPO'] = repository
os.environ['BORG_PASSPHRASE'] = password

# The main menu starts there
while chosen_activity != 0:
    print("What would you like to do?")
    # Start the chosen activity and go back to the activity selector.
    print("1: List Backups, 2: Show archive details, 3: Mount Archive, "
          "4: Restore Backup, 0: Exit")
    try:
        chosen_activity = int(input("Choose the desired activity: "))
        if chosen_activity == 1:
            # prints all the archives in the repository and lists them with
            # less
            os.system('borg list | less')
        if chosen_activity == 2:
            # Displays all the information related to the archive name the user 
            # enters
            archive_name = input("Please enter the archive name: ")
            os.system('borg info ::' + archive_name)
        if chosen_activity == 3:
            # mounts a chosen archive to /tmp/archive name
            archive_name = input("Please enter the archive name: ")
            mount_point = "/tmp/" + archive_name
            if not os.path.exists(mount_point):
                    os.makedirs(mount_point)
            os.system('borg mount  ::' + archive_name + " " + mount_point)
            print()
            print("Archive mounted at " + mount_point + "/")
            print()
        if chosen_activity == 4:
            archive_name = input("Please enter the archive name: ")
            restore_path = input("Please enter the path where you want to "
                                 "restore to: ")
            if not os.path.exists(restore_path):
                os.makedirs(restore_path)
            p = subprocess.Popen(['borg', 'extract', '::' + archive_name]
                ,cwd=restore_path)
            p.wait()
            print()
            print("Archive extracted to " + restore_path)
            print()
        elif chosen_activity == 0:
            if (not mount_point):
                print()
            else:
                print()
                print("Unmount Archive and remove folder.")
                print()
                os.system('fusermount -u' + " " + mount_point)
                os.rmdir(mount_point)
    except ValueError:
        print("Please enter a full number.")
