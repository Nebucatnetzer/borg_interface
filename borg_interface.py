#!/usr/bin/env python3
import os
import configparser
import subprocess

chosen_activity = None
mount_point = None

def list_archives():
    os.system('borg list | less')

def show_info():
    archive_name = input("Please enter the archive name: ")
    os.system('clear')
    os.system('borg info ::' + archive_name)
    print()
    input("Press a key to continue.")

def mount_archive():
    global mount_point
    archive_name = input("Please enter the archive name: ")
    mount_point = "/tmp/" + archive_name
    if not os.path.exists(mount_point):
            os.makedirs(mount_point)
    os.system('borg mount  ::' + archive_name + " " + mount_point)
    print()
    print("Archive mounted at " + mount_point + "/")
    print()

def restore_archive():
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

def configuration():
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

def exit():
    global mount_point
    if (not mount_point):
        print()
    else:
        print()
        print("Unmount Archive and remove folder.")
        print()
        os.system('fusermount -u' + " " + mount_point)
        os.rmdir(mount_point)

# The main menu starts there
configuration()
while chosen_activity != 0:
    os.system('clear')
    print("What would you like to do?")
    # Start the chosen activity and go back to the activity selector.
    print("1: List Backups, 2: Show archive details, 3: Mount Archive, "
          "4: Restore Backup, 0: Exit")
    try:
        chosen_activity = int(input("Choose the desired activity: "))
        if chosen_activity == 1:
            # prints all the archives in the repository and lists them with
            # less
            list_archives()
        if chosen_activity == 2:
            # Displays all the information related to the archive name the user 
            # enters
            show_info()
        if chosen_activity == 3:
            # mounts a chosen archive to /tmp/archive name
            mount_archive()
        if chosen_activity == 4:
           restore_archive()
        elif chosen_activity == 0:
           exit()
    except ValueError:
        print("Please enter a full number.")
