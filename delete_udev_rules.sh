#!/bin/bash

echo "◯ delete remap the device"
echo "sudo rm   /etc/udev/rules.d/capf.rules"
sudo rm   /etc/udev/rules.d/capf.rules
echo " "
echo "●︎ Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "○ finish  delete"