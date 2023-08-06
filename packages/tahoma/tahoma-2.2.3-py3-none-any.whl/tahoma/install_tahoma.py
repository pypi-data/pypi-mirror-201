#!/usr/bin/python3
import os

def main() :
    destination_folder=$HOME/
    print("This script will install Tahoma to the folder :\n "+$HOME+"/"+os.dirname(filename)")
    print("Press any key to continue or Esc to cancel...")
    notification = input()
    shutil.copy(os.path.dirname(filename),$HOME)
    print("Do you want to add the file "+os.dirname(filename)+" to the PATH, in order to use tahoma without entering the directory name "+$HOME+"/3"+os.dirname(filename)+" each time ? (Y or N)"
    notification=input()
    if notification.lower() == 'y'or notification.lower() == 'yes':

try:
    main()
    exit(0)
except Exception as e:
    print(e)
    exit(1)
