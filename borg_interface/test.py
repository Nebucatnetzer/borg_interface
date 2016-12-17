import subprocess
import socket
import time
import interface_functions
import sys

path_to_backup = "/home/andreas/"
archive_name = (socket.gethostname() + "-home"
                                     + time.strftime("_%Y-%m-%d_%H:%M"))

p = subprocess.Popen(['borg', 'create', '--exclude', '/home/andreas/.cache',
                      '--exclude', '/home/andreas/Downloads',
                      '::' + archive_name, path_to_backup], stderr=subprocess.PIPE)
p.wait()

sys.exit(0)
