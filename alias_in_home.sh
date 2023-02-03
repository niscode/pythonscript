#!/bin/sh
cd ~/
ln -s pythonscript/login_capf.sh
ln -s pythonscript/launch_client.sh
ln -s pythonscript/run_chimeSwitch.sh
ln -s pythonscript/gitpull_pythonscript.sh
ln -s pythonscript/get_output.sh
ln -s pythonscript/get_input.sh

# move autostart config files
cp ~/nano_scripts/autostart/* ~/.config/autostart/