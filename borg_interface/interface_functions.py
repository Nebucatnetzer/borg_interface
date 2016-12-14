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
    pause()

def mount_archive():
    archive_name = input("Please enter the archive name: ")
    int_vars.mount_point = "/tmp/" + archive_name
    if not os.path.exists(int_vars.mount_point):
            os.makedirs(int_vars.mount_point)
    os.system('borg mount  ::' + archive_name + " " + int_vars.mount_point)
    print()
    print("Archive mounted at " + int_vars.mount_point + "/.")
    print("The archive will remain mounted as long this programm is running.")
    print()
    pause()

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
    pause()

def configuration():
    # setup the config parser
    config = configparser.ConfigParser()
    # check whether the config file exists either in the home folder or next to
    # the binary
    home = os.getenv('HOME')
    if os.path.isfile(home + '/.config/borg_interface/borg_interface.cfg'):
        config.read(home + '/.config/borg_interface/borg_interface.cfg')
    elif os.path.isfile(home + '/.borg_interface.cfg'):
        config.read(home + '/.borg_interface.cfg')
    elif os.path.isfile('borg_interface.cfg'):
        config.read('borg_interface.cfg')
    else:
        print("Configuration file not found.")
        quit()
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
    else:
        print()
        print("Unmount Archive and remove folder.")
        print()
        os.system('fusermount -u' + " " + int_vars.mount_point)
        os.rmdir(int_vars.mount_point)

def pause():
    input("Press any key to continue.")
