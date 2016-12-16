#!/usr/bin/env python3
import os
import interface_functions
import interface_variables
import curses
chosen_activity = None

# The main menu starts there
interface_functions.configuration()
while chosen_activity != 0:
    interface_functions.draw_menu()
    screen = curses.initscr()
    try:
        chosen_activity = screen.getch()
        if chosen_activity == ord('1'):
            # prints all the archives in the repository and lists them with
            # less
            interface_functions.list_archives()
        if chosen_activity == ord('2'):
            # Displays all the information related to the archive name the user 
            # enters
            interface_functions.show_info()
        if chosen_activity == ord('3'):
            # mounts a chosen archive to /tmp/archive name
            interface_functions.mount_archive()
        if chosen_activity == ord('4'):
           interface_functions.restore_archive()
        elif chosen_activity == ord('0'):
           interface_functions.exit()
    except ValueError:
        print("Please enter a full number.")
