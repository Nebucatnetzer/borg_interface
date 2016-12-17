import os
import sys
import configparser
import subprocess
import interface_variables
import curses

int_vars = interface_variables


def get_param(prompt_string):
    screen = curses.initscr()
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(3, 2, 60)
    return input


def draw_menu():
    screen = curses.initscr()
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, "Please enter a number...")
    screen.addstr(4, 4, "1 - List archives in repository")
    screen.addstr(5, 4, "2 - Show archive details")
    screen.addstr(6, 4, "3 - Mount archive")
    screen.addstr(7, 4, "4 - Restore an archive to specific location")
    screen.addstr(8, 4, "5 - Delete an archive")
    screen.addstr(9, 4, "6 - Create a backup")
    screen.addstr(10, 4, "0 - Exit")
    screen.refresh()


def draw_screen(r, c, message):
    screen = curses.initscr()
    screen.clear()
    screen.border(0)
    screen.addstr(r, c, message)
    screen.refresh()


def list_archives():
    curses.endwin()
    borg_list = subprocess.Popen(['borg', 'list'], stdout=subprocess.PIPE)
    less_output = subprocess.Popen(['less'], stdin=borg_list.stdout)
    borg_list.wait()
    less_output.wait()


def show_info():
    archive_name = get_param("Please enter the archive name: ").decode('utf-8')
    curses.endwin()
    os.system('clear')
    p = subprocess.Popen(['borg', 'info', '::' + archive_name])
    p.wait()
    pause()


def mount_archive():
    screen = curses.initscr()
    archive_name = get_param("Please enter the archive name: ").decode('utf-8')
    int_vars.mount_point = os.path.join('/tmp', archive_name)
    if not os.path.exists(int_vars.mount_point):
        os.makedirs(int_vars.mount_point)
    p = subprocess.Popen(['borg', 'mount', '::' + archive_name,
                          int_vars.mount_point])
    p.wait()
    draw_screen(2, 2, "Archive mounted at " + int_vars.mount_point + "/.")
    screen.addstr(3, 2, "The archive will remain mounted as long this program "
                        "is running.")
    screen.refresh()
    ncurses_pause(5)


def restore_archive():
    archive_name = get_param("Please enter the archive name: ").decode('utf-8')
    restore_path = get_param("Please enter the path where you want to "
                             "restore to: ").decode('utf-8')
    draw_screen(2, 2, "Please wait while the archive gets restored.")
    if not os.path.exists(restore_path):
        os.makedirs(restore_path)
    p = subprocess.Popen(['borg', 'extract', '::' + archive_name]
                         , cwd=restore_path)
    p.wait()
    draw_screen(2, 2, "Archive extracted to " + restore_path)
    ncurses_pause(5)


def delete_archive():
    archive_name = get_param("Please enter the archive name: ").decode('utf-8')
    draw_screen(2, 2, "Please wait while the archive gets deleted.")
    p = subprocess.Popen(['borg', 'delete', '::' + archive_name])
    p.wait()
    draw_screen(2, 2, "Archive " + archive_name + " deleted")
    ncurses_pause(5)


def create_archive():
    archive_name = get_param("Please enter an archive name: ").decode('utf-8')
    path_to_backup = get_param("Please enter the "
                               "path to backup: ").decode('utf-8')
    draw_screen(2, 2, "Please wait while the backup gets created.")
    p = subprocess.Popen(['borg', 'create', '::' + archive_name,
                          path_to_backup])
    p.wait()
    draw_screen(2, 2, "Archive of " + path_to_backup + " created.")
    ncurses_pause(5)


def configuration():
    # setup the config parser
    config = configparser.ConfigParser()
    # check whether the config file exists either in the home folder or next to
    # the binary
    home = os.getenv('HOME')
    config_file = "borg_interface.cfg"
    config_folder = ".config/borg_interface/"
    config_path = os.path.join(home, config_folder, config_file)
    if os.path.isfile(config_path):
        config.read(config_path)
    elif os.path.isfile(config_file):
        config.read(config_file)
    else:
        print("Configuration file not found.")
        sys.exit(0)
    # assign the repository variable depending whether it's a remote or a local
    # repository
    if 'server' in config['DEFAULT']:
        repository = (config['DEFAULT']['user']
                      + "@"
                      + config['DEFAULT']['server']
                      + ":"
                      + config['DEFAULT']['repository_path'])
        int_vars.server = config['DEFAULT']['server']
    else:
        repository = config['DEFAULT']['repository_path']
    # assign the password variable
    password = config['DEFAULT']['password']
    # set the environment variables
    os.environ['BORG_REPO'] = repository
    os.environ['BORG_PASSPHRASE'] = password


def exit():
    if not int_vars.mount_point:
        curses.endwin()
        os.system('clear')
        sys.exit(0)
    else:
        curses.endwin()
        os.system('clear')
        print("Unmount Archive and remove folder.")
        print()
        os.system('fusermount -u' + " " + int_vars.mount_point)
        os.rmdir(int_vars.mount_point)
        sys.exit(0)


def ncurses_pause(c):
    screen = curses.initscr()
    screen.border(0)
    screen.addstr(c, 2, "Press Enter to continue...")
    screen.refresh()
    input = screen.getstr(3, 2, 60)
    return input


def pause():
    input("Press Enter to continue...")
