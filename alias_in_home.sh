#!/bin/sh
cd ~/
ln -s pythonscript/capf_login.sh
#ln -s pythonscript/launch_client.sh
ln -s pythonscript/launch_bridge.sh
ln -s pythonscript/run_chimeSwitch.sh
ln -s pythonscript/gitpull_pythonscript.sh
ln -s pythonscript/get_output.sh
ln -s pythonscript/get_input.sh

# move autostart config files
cp ~/pythonscript/autostart/* ~/.config/autostart/

echo "エイリアスの作成が終了しました。続いてpythonライブラリを取得します。"

cd ~/pythonscript/
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y python3-pip
pip3 install --upgrade pip
pip3 install -r requirements.txt
