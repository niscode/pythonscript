#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
import collections
import time
from threading import Thread
import socket
# import sounddevice as sd    # un usefor Jetson
import tkinter as tk
import WebSocketCapf as cwebsock
import json

# スクレイピング用
import requests
from bs4 import BeautifulSoup

# ボタン取得用
import evdev
DEVICE_PATH = "/dev/input/callButton"   # デバイスの指定


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
    def __init__(self, loginurl, selfID, selfIDPasswd, websockurl, robotIP, robotPort, targetID) :
        super(websocketagent, self).__init__(loginurl, selfID, selfIDPasswd, websockurl)

        self.robotIP = robotIP
        self.robotPort = robotPort
        self.setMessageCallback(self.sendMessageCB)

        self.selfID = selfID
        self.targetID = targetID


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
        print("[Command from CAPF]   " + message)

        if 'EventInfo' in message:
            response = requests.get('https://startupside.jp/tokyo/event/')
            soup = BeautifulSoup(response.text, 'html.parser')
            # イベント名を取得
            event_title = soup.find('h3', attrs={'class':'eventBox_title'}).get_text()
            # 日程を取得   時間は未取得
            event_date = event_title[event_title.rfind('　')+1:event_title.rfind('催')+1]
            event_date = event_date.replace("(", "")
            event_date = event_date.replace(")", "曜日に")
            
            event_title = event_title.replace(event_title[event_title.rfind('　'):len(event_title)+1], "")
            print(event_title)
            print(event_date)
            
            # イベントの種類を取得
            event_type = soup.find('li', attrs={'class':'eventBox_type'}).get_text()
            print(event_type)
            # コマンド内容を書き換え
            message = (message + ";" + event_title + ";" + event_date + ";" +event_type)

        cmd = message.strip()
        robotThread = Thread(target=robotCmdSend,
            args=(self.robotIP, self.robotPort, cmd))
        robotThread.start()


    def callOperator(self):
        device = evdev.InputDevice(DEVICE_PATH)
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.value == 1:
                    if event.code == 183:
                        print("[USB Button] - pushed!")
                        jsonparam = {'id' : self.selfID}
                        jsoncmd = {'cmd' : 'bell', 'param' : json.dumps(jsonparam)}
                        jsonmsg = {'targets' : [self.targetID], 'message' : json.dumps(jsoncmd)}
                        self.send(json.dumps(jsonmsg))
        # return


if __name__ == '__main__' :
    if len(sys.argv) < 8 :
        print("Usage: {} <login url> <id> <passwd> <websocket url> <robot-addr> <robot-port> <targetid>".format(sys.argv[0]))
        sys.exit(1)
    loginurl = sys.argv[1]
    loginid = sys.argv[2]
    loginpasswd = sys.argv[3]
    websockurl = sys.argv[4]
    robotaddr = sys.argv[5]
    robotport = int(sys.argv[6])
    targetid = sys.argv[7]

    agent = websocketagent(loginurl, loginid, loginpasswd, websockurl, robotaddr, robotport, targetid)

    if not agent.connect() :
        print('cannot connect websocket')
        sys.exit(0)

    while agent.isactive() :
        callThread = Thread(target=agent.callOperator())
        callThread.start()
        time.sleep(1)