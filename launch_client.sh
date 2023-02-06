#!/bin/sh
# python3 ~/pythonscript/webagent/webagent.py "https://ignis2.ca-platform.org/api/login" "CA003" "CA003" "wss://ignis2-websocket.ca-platform.org" "192.168.10.4" 5001

### for Linux --- just TCP socket connection
python3 ~/pythonscript/client.py CA001 ignis2-sock.ca-platform.org 11001 192.168.10.2 5001


### for macOS / windows
# python client.py CA001 ignis2-sock.ca-platform.org 11001 192.168.11.18 5001
