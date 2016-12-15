import os
import sys
import configparser
import subprocess
import interface_variables

int_vars = interface_variables

def list_archives():
    borg_list = subprocess.Popen(['borg', 'list'], stdout=subprocess.PIPE)
    less_output = subprocess.Popen(['less'], stdin=borg_list.stdout)
    borg_list.wait()
    less_output.wait()

def show_info():
    prompt_archive_name()
    os.system('clear')
    p = subprocess.Popen(['borg', 'info', '::' + int_vars.archive_name])
    p.wait()
    print()
    pause()

def mount_archive():
    prompt_archive_name()
    int_vars.mount_point = "/tmp/" + int_vars.archive_name
    if not os.path.exists(int_vars.mount_point):
            os.makedirs(int_vars.mount_point)
    p = subprocess.Popen(['borg', 'mount', '::' + int_vars.archive_name,
                          int_vars.mount_point])
    p.wait()
    print()
    print("Archive mounted at " + int_vars.mount_point + "/.")
    print("The archive will remain mounted as long this programm is running.")
    print()
    pause()

def restore_archive():
    prompt_archive_name()
    restore_path = input("Please enter the path where you want to "
                         "restore to: ")
    if not os.path.exists(restore_path):
        os.makedirs(restore_path)
    p = subprocess.Popen(['borg', 'extract', '::' + int_vars.archive_name]
        ,cwd=restore_path)
    p.wait()
    print()
    print("Archive extracted to " + restore_path)
    print()
    pause()

def configuration():
    # setup the config parser
    config = configparser.ConfigParser()
    # check whether the config file exists either in the home folder or next to
    # the binary
    home = os.getenv('HOME')
    config_file = "borg_interface.cfg"
    config_long_path =  os.path.join(home, ".config/borg_interface/",
                                     config_file)
    if os.path.isfile(config_long_path):
        config.read(config_long_path)
    elif os.path.isfile(config_file):
        config.read(config_file)
    else:
        print("Configuration file not found.")
        sys.exit(1)
    # assign the repository variable depending wheter it's a remote or a local
    # repository
    if 'server' in config['DEFAULT']:
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
    if (not int_vars.mount_point):
        print()
        sys.exit(0)
    else:
        print()
        print("Unmount Archive and remove folder.")
        print()
        os.system('fusermount -u' + " " + int_vars.mount_point)
        os.rmdir(int_vars.mount_point)
        sys.exit(0)

def pause():
    input("Press any key to continue.")

def prompt_archive_name():
    int_vars.archive_name = input("Please enter the archive name: ")
