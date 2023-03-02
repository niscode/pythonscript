#!/bin/sh
cd ~/
ln -s pythonscript/capf_login.sh
ln -s pythonscript/webagent/launch_ws.sh
#ln -s pythonscript/launch_client.sh
# ln -s pythonscript/run_chimeSwitch.sh
ln -s pythonscript/gitpull_pythonscript.sh
ln -s pythonscript/get_output.sh
ln -s pythonscript/get_input.sh
echo "エイリアスの作成が終了しました。"

# move autostart config files
cp ~/pythonscript/autostart/* ~/.config/autostart/