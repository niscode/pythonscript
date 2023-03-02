#!/bin/sh
# 引数の指定: <login url> <id> <passwd> <websocket url> <robot-addr> <robot-port> <targetid>

python3 ~/pythonscript/webagent.py "https://ignis2.ca-platform.org/api/login" "CA003" "CA003" "wss://ignis2-websocket.ca-platform.org" "192.168.10.4" 5001 'OP002SA'