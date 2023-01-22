#!/bin/sh
### for Linux

# python3 ~/pythonscript/tkinter_ChimeSwitch.py CA000 ignis2-sock.ca-platform.org 11001 CA010
echo 'capf' | sudo -S python3 ~/pythonscript/keyboard_ChimeSwitch.py CA000 ignis2-sock.ca-platform.org 11001 CA010
#sudo python3 /home/orin/pythonscript/ChimeSwitch_Linux.py CA000 ignis2-sock.ca-platform.org 11001 CA010

# sudo python3 ~/pythonscript/ChimeSwitch_Linux.py CA000 ignis2-sock.ca-platform.org 11001 CA010