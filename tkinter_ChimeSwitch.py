#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# for Linux

# import keyboard
import tkinter as tk
import matplotlib

import ctypes
import sys
import socket
import select
import time
from datetime import datetime, timedelta

root = tk.Tk()
# root.option_add('*font', ('', 14))
canvas = tk.Canvas(root, borderwidth=0)
frame = tk.Frame(canvas)



def keypress(event):
    renderkey()
    print(renderkey())

    # global count
    if event.keysym == 'unknown':
        F13_pushed = 1
        # count += 1
        print("[*] F13 pressed.")
        serversoc.send(msg)
        lastCommu = datetime.now()
        # try :
        #     if (count % 2 == 1):
        #         print("一回のプッシュで複数回いかれてます？")
                
        # except :
        #     print('Serverとの通信に失敗しました - 01。再接続します :', datetime.now())
        #     break
    else:
        print("[* {} is pushed...]".format(event.keysym))
        return


def loop(serversoc, sid, targetid):
    msg = (targetid + '-cmd;action;chime\n').encode('utf-8')
    nopmsg = (targetid + '-cmd;nop\n').encode('utf-8')
    lastCommu = datetime.now()
    #readfds = list([serversoc])
    count = 0
    while True:
        try:
            rready, _, _ = select.select([serversoc], [], [], 0)
            if serversoc in rready :
                recv = serversoc.recv(4096).decode()
                # コマンドは受け付けていないのでここでは何もしない。サーバーから接続維持用のパケットが飛んできたときのための処理
                print(recv)
        finally :
            pass

        if datetime.now() > lastCommu + timedelta(seconds=60.0) :
            try :
                serversoc.send(nopmsg)
                lastCommu = datetime.now()
            except:
                print('Serverとの通信に失敗しました - 02。再接続します :', datetime.now())
                break


if __name__ == '__main__':
    if (len(sys.argv) != 5):
        print("Usage: {} <id> <server ip> <server port> <target id>".format(sys.argv[0]))
        sys.exit(1)

    sid = sys.argv[1]
    serverip = sys.argv[2]
    serverport = sys.argv[3]
    targetid = sys.argv[4]
    server = (serverip, int(serverport))

    while True : 
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            soc.connect(server)
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            root.bind('<KeyPress>', keypress)
        except:
            print('serverとの接続に失敗しました - 03。 : %s:%s' % (serverip, serverport))
            soc = None
            time.sleep(1.0)
            continue

        try:
            data = soc.recv(4096).decode()
            print(str(data))
            cmd = str(data.rstrip())
            line = 'id;%s' % sid
            soc.send(line.encode('utf-8'))
        except:
            print('サーバーとの通信に失敗しました - 04。再接続します :', datetime.now())
            soc = None
            continue
            #sys.exit(0)
        loop(soc, sid, targetid)
        soc.close()
        soc = None
