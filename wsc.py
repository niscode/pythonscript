# coding: utf-8

import sys
import socket
import time
import websocket
import threading
import select
import ssl
from datetime import datetime, timedelta
import json
import rel
import requests


def sendJsonCommand(ws, index):
    commands = jsonCommands[index]
    for msg in commands:
        print(msg)
        if(type(msg) is dict):
            ws.send(json.dumps(msg))
        else:
            cols = msg.split('/wait')
            millisec = int(cols[1])
            time.sleep(millisec / 1000.0)

# j -> for handai system
def on_message_j(ws, message):
    print('M:', message)

def on_error_j(ws, error):
    print('E:', error)

def on_close_j(ws):
    print("Closing")

def on_open_j(ws):
    print("openning")
    # sendJsonCommand(ws, 6)


# no j -> for capf
def on_error(ws, error):
    print('Ex:', error)

def on_close(ws):
    print("Closing")

def on_open(ws):
    print("openning")


def on_message(ws, message):
    global cws
    global addr
    global port
    global scenario
    scenario = ''

    if message == 'something' : return
    print('M:', message, addr, port, cws)
    sota = (addr, port)
    cmd = message
    # print(cmd)
    header = message[:1]

    # 音声案内コマンド 18 items   先頭 11items はブース紹介用 -- 2022/10/28  -- 2022/10/28
    if header == "V" :
        if cmd == "V_Self" :
            sendJsonCommand(cws, 0)
        else :
            num_i = 0
            while cmd != V_cmdlist[num_i][0] :
                num_i += 1
            scenario = V_cmdlist[num_i][1]

            if num_i < 11 :
                sendJsonCommand(cws, num_i + 1)
                print ('\033[34m' + V_cmdlist[num_i][0] + ' 音声案内のコマンドを受け取ったよ。ブースの紹介文を発話するね: \n' + scenario + '\033[0m')
                print()
            else :
                sendJsonCommand(cws, num_i + 1)
                print ('\033[34m' + V_cmdlist[num_i][0] + ' 音声案内のコマンドを受け取ったよ。場所の案内を開始するね: \n' + scenario + '\033[0m')

    if header == "H" :
        if cmd == "H_short1" :
            sendJsonCommand(cws, 27)
            print ('\033[34m' + ' 短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short2" :
            sendJsonCommand(cws, 28)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short3" :
            sendJsonCommand(cws, 29)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short4" :
            sendJsonCommand(cws, 30)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short5" :
            sendJsonCommand(cws, 31)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')


    # 動作コマンド 14 items   先頭 6items はナビゲーション用 -- 2022/10/28
    if header == "M" :
    #global ad
        num_j = 0
        while cmd != M
    #global adist[num_j] :
            num_j += 1
    #global ad

        if num_j < 7 :
            client.cancel_goal()    #実行中のnavigationを中断するリクエスト
            try:
                goal_pose = MoveBaseGoal()
                goal_pose.target_pose.header.frame_id = 'map'
                goal_pose.target_pose.pose.position.x = nav_dict[cmd][0]
                goal_pose.target_pose.pose.position.y = nav_dict[cmd][1]
                goal_pose.target_pose.pose.position.z = nav_dict[cmd][2]
                goal_pose.target_pose.pose.orientation.x = nav_dict[cmd][3]
                goal_pose.target_pose.pose.orientation.y = nav_dict[cmd][4]
                goal_pose.target_pose.pose.orientation.z = nav_dict[cmd][5]
                goal_pose.target_pose.pose.orientation.w = nav_dict[cmd][6]
                #clientとしてgoalをサーバーに送ると同時にfeedback_cb関数を呼び出す
                result = client.send_goal(goal_pose)
                print ('\033[32m' + M_cmdlist[num_j] + ' ... ナビゲーションを実行するね。' + '\033[0m')
                if result:
                    print(r
    #global adesult)
                    rospy.loginfo("Goal execution done!")
            except rospy.ROSInterruptException:
                rospy.loginfo("Navigation test finished.")

        else :
            sendJsonCommand(cws, num_j + 12)
            print ('\033[32m' + '動作コマンド ' + M_cmdlist[num_j] + ' を実行するね' + '\033[0m')


    else :
    #global ad
        if cmd == "cmd;Forw
    #global adard" or cmd == "cmd;TurnLeft" or cmd == "cmd;TurnRight" or cmd == "cmd;Backward" or cmd == "cmd;Stop":
            print ('\033[33
    #global adm' + cmd + ' ... マニュアルモードで移動するよ。' + '\033[0m')
            p=rospy.Publish
    #global ader('rover_twist',Twist, queue_size=10)
            rate = rospy.Rate(10)

            x = moveBindings[cmd][0]
            y = moveBindings[cmd][1]
            z = moveBindings[cmd][2]
            th = moveBindings[cmd][3]
            
            t = Twist()
            t.linear.x = x * 0.1
            t.linear.y = y * 0.1
            t.linear.z = z * 0.1
            t.angular.x = 0
            t.angular.y = 0
            t.angular.z = th * 0.2
            
            for i in range(0, 5) :
                p.publish(t)
                rate.sleep()
        
        # print(cmd)
        if cmd == "cmd;scenario;self_intro" :
            sendJsonCommand(cws, 0)

if __name__ == '__main__':
    print(ros_msg)
    #global cws
    #global addr
    #global port

    if (len(sys.argv) != 9):
        # socket --- 1 device (argv == 6)
        # print("Usage: {} <id> <server ip> <server port> <controller ip> <controller port>".format(sys.argv[0]))
        # python3 ~/pythonscript/client.py CA001 atr-dev01-sock.ca-platform.org 11001 192.168.10.2 5001

        # web-socket --- 1 device
        print("Usage: {} <login url> <id> <passwd> <websocket url> <jetson ip> <jetson port> <handaisys ip> <handaisys port>".format(sys.argv[0]))
        # python3 ~/scripts/wsc.py "https://hanazono.ca-platform.org/api/login" "CA001" "CA001" "wss://hanazono-websocket.ca-platform.org" "10.186.42.91" "5001"

        # web-socket --- 2 devices
        # print("Usage: {} <login url> <id> <passwd> <websocket url> <jetson ip> <jetson port> <handaisys ip> <handaisys port>".format(sys.argv[0]))
        # python3 ~/scripts/wsc-json-ATR.py "https://hanazono.ca-platform.org/api/login" "CA001" "CA001" "wss://hanazono-websocket.ca-platform.org" "10.186.42.91" "1890" "10.186.42.31" "11920"
        sys.exit(1)

    login_url = sys.argv[1]
    sid = sys.argv[2]
    passwd = sys.argv[3]

    websockurl = sys.argv[4]
    addr = sys.argv[5]
    port = int(sys.argv[6])
    handaiip = (sys.argv[7], int(sys.argv[8]))
    websocket.enableTrace(True)

    print('handai =', handaiip)
    cws = websocket.WebSocketApp("ws://%s:%d/command" %( handaiip[0], handaiip[1]),
                              on_message = on_message_j,
                              on_error = on_error_j,
                              on_close = on_close_j)
    #cws.on_open = on_open_j
    cwst = threading.Thread(target=cws.run_forever)
    cwst.daemon = True
    cwst.start()

    payload = {"name" : sid, "password" : passwd}
    r = requests.post(login_url, params = payload)
    authorisation = json.loads(r.text)["authorisation"]
    token = authorisation["token"]
    ws = websocket.WebSocketApp(websockurl + "?token=" + token,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    wst = threading.Thread(target = ws.run_forever)
    wst.daemon = True
    wst.start()
    try:
        while not rospy.is_shutdown():
        # while True :
            time.sleep(1.0)
    except KeyboardInterrupt:
        print('Ctrl-C を受け取りました。プログラムを終了します,,,,,,')
        sys.exit(1)