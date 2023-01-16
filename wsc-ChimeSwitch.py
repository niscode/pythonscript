# Event types
types = {
    0x01 : 'KEY',
}

# # Keys and buttons
keys = {
    0: 'RESERVED',
    1: 'ESC',
    2: '1',
    183 : 'F13',
}

actions = {
    0 : 'UP',
    1 : 'DOWN',
    2 : 'HELD',
}
#############

import sys
import io
import socket
import time
# import websocket
import select
# import ctypes
from ctypes import Structure, sizeof, c_long, c_int32, c_uint16
from datetime import datetime, timedelta

class TimeVal(Structure):
    _fields_ = (
        ("tv_sec", c_long),
        ("tv_usec", c_long),
    )

class InputEvent(Structure):
    _fields_ = (
        ('time', TimeVal),
        ('type', c_uint16),
        ('code', c_uint16),
        ('value', c_int32),
    )

event_size = sizeof(InputEvent)

# イベントを読み込んで構造体を作って返す関数
def get_input_event_struct(f):
    ie = io.BytesIO(f.read(event_size))
    struct_ie = InputEvent()
    ie.readinto(struct_ie)
    return struct_ie

# 押されているキーを格納する集合
pressed_keys = set()

# ホットキーを検知する関数
def detect_hotkey(hotkeys_dict, key, action):
    global pressed_keys
    # キーが放されたら集合から消す
    if action == 'UP':
        pressed_keys.remove(key)
    # キーが押されたら集合に加える
    elif action == 'DOWN':
        pressed_keys.add(key)
    else: # 長押しは無視
        return None
    # 押されているキーがホットキーとマッチするか確認
    for message, hotkey in hotkeys_dict.items():
        if hotkey == pressed_keys:
            # マッチしていたら対応するメッセージを返す
            return message 
    return None


# if __name__ == '__main__':
'''
def checkKey() :
    result = False
    try :
        #F13 => 0x7c
        if ctypes.windll.user32.GetAsyncKeyState(0x7c) == 0x8000 :
            result = True
    except KeyboardInterrupt :
        pass

    return result
'''

def loop(serversoc, sid, targetid):
    msg = (targetid + '-cmd;action;chime\n').encode('utf-8')
    nopmsg = (targetid + '-cmd;nop\n').encode('utf-8')
    lastCommu = datetime.now()
    #readfds = list([serversoc])
    while True:
        try:
            rready, _, _ = select.select([serversoc], [], [], 0)
            if serversoc in rready :
                recv = serversoc.recv(4096).decode()
                # コマンドは受け付けていないのでここでは何もしない。サーバーから接続維持用のパケットが飛んできたときのための処理
                print(recv)
        finally :
            pass


        # 入力デバイスイベントファイル
        dev_input_file = '/dev/input/event0'
        # メッセージに対応するホットキー集合のマッピング
        hotkeys_dict = {
                'F13 is pushed.' : {'F13'}
            }
        print('Hotkeys:', list(hotkeys_dict.values()))

        # イベントファイルをオープン
        with open(dev_input_file, mode='rb', buffering=1) as f:
            # 無限ループで監視し続けること
            # while True:
            # バイト列を構造体に入れる
            struct_ie = get_input_event_struct(f)
            # キーイベントかどうかの判定
            if struct_ie.type == 0x01: # key event type
                # キーコードからキー名に変換
                key = keys.get(struct_ie.code)
                if key is None:
                    continue
                # バリューからアクション名に変換
                action = actions.get(struct_ie.value)
                if action is None:
                    continue

                # ホットキー検出関数に渡す
                message = detect_hotkey(hotkeys_dict, key, action)
                if message is not None:
                    print(message)


        # if checkKey() :
        #     try :
        #         serversoc.send(msg)
        #         lastCommu = datetime.now()
        #     except :
        #         print('Serverとの通信に失敗しました - 01。再接続します :', datetime.now())
        #         break
        #     while checkKey():
        #         pass

        if datetime.now() > lastCommu + timedelta(seconds=60.0) :
            try :
                serversoc.send(nopmsg)
                lastCommu = datetime.now()
            except:
                print('Serverとの通信に失敗しました - 02。再接続します :', datetime.now())
                break


if __name__ == '__main__':
    if (len(sys.argv) != 5):        print("Usage: {} <id> <server ip> <server port> <controller ip> <controller port>".format(sys.argv[0]))

        ## socket --- 1 device (argv == 5)
        print("Usage: {} <id> <server ip> <server port> <target id>".format(sys.argv[0]))

        ## web-socket --- 1 device
        # print("Usage: {} <login url> <id> <passwd> <websocket url> <jetson ip> <jetson port> <handaisys ip> <handaisys port>".format(sys.argv[0]))
        ## python3 ~/scripts/wsc.py "https://hanazono.ca-platform.org/api/login" "CA001" "CA001" "wss://hanazono-websocket.ca-platform.org" "10.186.42.91" "5001"
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