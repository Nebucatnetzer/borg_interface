import os
import configparser
import subprocess
import interface_variables

int_vars = interface_variables

def list_archives():
    os.system('borg list | less')

def show_info():
    archive_name = input("Please enter the archive name: ")
    os.system('clear')
    os.system('borg info ::' + archive_name)
    print()
    input("Press a key to continue.")

def mount_archive():
    archive_name = input("Please enter the archive name: ")
    int_vars.mount_point = "/tmp/" + archive_name
    if not os.path.exists(int_vars.mount_point):
            os.makedirs(int_vars.mount_point)
    os.system('borg mount  ::' + archive_name + " " + int_vars.mount_point)
    print()
    print("Archive mounted at " + int_vars.mount_point + "/")
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
    if 'server' in config['DEFAULT']:
        repository = (config['DEFAULT']['user']
                     + "@"
                     + config['DEFAULT']['server']
                     + ":"
                     + config['DEFAULT']['repository_path'])
        print("remote archive")
    else:
        repository = config['DEFAULT']['repository_path']
        print("local archive")
    input()
    # assign the password variable
    password = config['DEFAULT']['password']
    # set the environment variables
    os.environ['BORG_REPO'] = repository
    os.environ['BORG_PASSPHRASE'] = password

def exit():
    if (not int_vars.mount_point):
        print()
    else:
        print()
        print("Unmount Archive and remove folder.")
        print()
        os.system('fusermount -u' + " " + int_vars.mount_point)
        os.rmdir(int_vars.mount_point)
