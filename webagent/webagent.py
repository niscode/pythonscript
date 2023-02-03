# -*- config:utf-8 -*-

import sys
from datetime import datetime, timedelta
import collections
import time
from threading import Thread
import socket
import sounddevice as sd
import tkinter as tk
import WebSocketCapf as cwebsock
import json

def robotCmdSend(ip, port, cmd):
    # ロボットへの送信時にネットワーク異常の場合ブロックが発生してしまう可能性があるので別スレッドで処理する。
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #print((ip,port))
        client.connect((ip, port))
        #print(cmd)
        client.send(cmd.encode('utf-8'))
    except socket.error as e:
        print('robotとの通信に失敗しました。', e)
    finally:
        client.close()


class websocketagent(cwebsock.WebSocketCapf) :
    def __init__(self, loginurl, selfID, selfIDPasswd, websockurl, robotIP, robotPort) :
        super(websocketagent, self).__init__(loginurl, selfID, selfIDPasswd, websockurl)
        self.robotIP = robotIP
        self.robotPort = robotPort
        self.setMessageCallback(self.sendMessageCB)
    
    def robotCmdSend(ip, port, cmd):
        # ロボットへの送信時にネットワーク異常の場合ブロックが発生してしまう可能性があるので別スレッドで処理する。
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            #print((ip,port))
            client.connect((ip, port))
            #print(cmd)
            client.send(cmd.encode('utf-8'))
        except socket.error as e:
            print('robotとの通信に失敗しました。', e)
        finally:
            client.close()

    def sendMessageCB(self, message) :
        def robotCmdSend(ip, port, cmd):
            # ロボットへの送信時にネットワーク異常の場合ブロックが発生してしまう可能性があるので別スレッドで処理する。
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((ip, port))
                client.send(cmd.encode('utf-8'))
            except socket.error as e:
                print('robotとの通信に失敗しました。', e)
            finally:
                client.close()
        print(message)
        cmd = message.strip()
        robotThread = Thread(target=robotCmdSend,
            args=(self.robotIP, self.robotPort, cmd))
        robotThread.start()

if __name__ == '__main__' :
    if len(sys.argv) < 7 :
        print("Usage: {} <login url> <id> <passwd> <websocket url> <robot-addr> <robot-port>".format(sys.argv[0]))
        sys.exit(1)
    loginurl = sys.argv[1]
    loginid = sys.argv[2]
    loginpasswd = sys.argv[3]
    websockurl = sys.argv[4]
    robotaddr = sys.argv[5]
    robotport = int(sys.argv[6])

    agent = websocketagent(loginurl, loginid, loginpasswd, websockurl, robotaddr, robotport)
    if not agent.connect() :
        print('cannot connect websocket')
        sys.exit(0)

    while agent.isactive() :
        time.sleep(1)
    
