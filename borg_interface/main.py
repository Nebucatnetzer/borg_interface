#!/usr/bin/env python3
import os
import interface_functions
import interface_variables

chosen_activity = None

# The main menu starts there
interface_functions.configuration()
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
            interface_functions.list_archives()
        if chosen_activity == 2:
            # Displays all the information related to the archive name the user 
            # enters
            interface_functions.show_info()
        if chosen_activity == 3:
            # mounts a chosen archive to /tmp/archive name
            interface_functions.mount_archive()
        if chosen_activity == 4:
           interface_functions.restore_archive()
        elif chosen_activity == 0:
           interface_functions.exit()
    except ValueError:
        print("Please enter a full number.")
