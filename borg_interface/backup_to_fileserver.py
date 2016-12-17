#!/usr/bin/env python3
import subprocess
import interface_functions
import interface_variables
import sys
import time
import socket

int_vars = interface_variables


def take_backup():
    response = subprocess.Popen(['ping', '-c', '1', 'fileserver.2li.local'])
    response.wait()
    returncode = response.returncode
    if returncode == 0:
        backup_home()
        backup_vms()
        prune_home()
        prune_vms()
    else:
        print("Server not available")
        sys.exit(0)


def backup_home():
    path_to_backup = "/home/andreas/"
    archive_name = (socket.gethostname() + "-home"
                    + time.strftime("_%Y-%m-%d_%H:%M"))

    p = subprocess.Popen(['borg', 'create', '--exclude', '/home/andreas/.cache',
                          '--exclude', '/home/andreas/Downloads',
                          '::' + archive_name, path_to_backup])
    p.wait()


def backup_vms():
    path_to_backup = "/mnt/sdc/VMs"
    archive_name = (socket.gethostname() + "-VMs"
                    + time.strftime("_%Y-%m-%d_%H:%M"))

    p = subprocess.Popen(['borg', 'create',
                          '::' + archive_name, path_to_backup])
    p.wait()


def prune_home():
    archive_name = (socket.gethostname() + "-home")
    p = subprocess.Popen(['borg', 'prune', '--prefix', archive_name,
                          '--keep-hourly=24', '--keep-daily=7',
                          '--keep-weekly=4', '--keep-monthly=12',
                          '--keep-yearly=1'])
    p.wait()


def prune_vms():
    archive_name = (socket.gethostname() + "-VMs")
    p = subprocess.Popen(['borg', 'prune', '--prefix', archive_name,
                          '--keep-hourly=24', '--keep-daily=7',
                          '--keep-weekly=4', '--keep-monthly=12',
                          '--keep-yearly=1'])
    p.wait()


interface_functions.configuration()
take_backup()
