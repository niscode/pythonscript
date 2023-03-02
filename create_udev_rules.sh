#!/bin/bash

echo "●︎ check it using the command : ls -l /dev|grep ttyUSB"
echo "●︎ start copy capf.rules to  /etc/udev/rules.d/"
sudo cp ~/pythonscript/capf.rules  /etc/udev/rules.d
echo " "
echo "●︎︎ Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "◯︎︎ finish︎"