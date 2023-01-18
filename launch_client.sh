#!/bin/sh

### for Linux
python3 ~/pythonscript/client.py CA001 ignis2-sock.ca-platform.org 11001 192.168.10.2 5001
# python3 ~/pythonscript/wsc.py CA001 ignis2-sock.ca-platform.org 11001 192.168.10.2 5001


### for macOS / windows
## itb-sota002
# python client.py CA001 ignis2-sock.ca-platform.org 11001 192.168.11.18 5001

## itb-sota008
#python client.py CA002 ignis2-sock.ca-platform.org 11001 192.168.11.19 5001

### developing ...
# python wsc.py "https://ignis2.ca-platform.org/api/login" "CA001" "CA001" "wss://hanazono-websocket.ca-platform.org" "localhost" "1890" "192.168.11.19" "11920"