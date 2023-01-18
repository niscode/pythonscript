import sys
import socket
from datetime import datetime
from playsound import playsound

# playsound は1.3は使わないこと
# pip install playsound==1.2.2
'''
def login(soc, sid):
    try:
        data = soc.recv(4096).decode()
        print(str(data))
        cmd = str(data.rstrip())
        line = 'id;%s' % sid
        soc.send(line.encode('utf-8'))
    except:
        print('サーバーとの通信に失敗しました。')
        sys.exit(0)
'''

def loop(serversoc):
    st = serversoc.makefile()
    while True:
        try:
            data = st.readline().strip()
        except socket.timeout:
            data = None
        if data is None : break
        cmd = str(data.rstrip())
        if len(cmd) == 0 : continue
        print(cmd)
        if cmd == 'cmd;action;chime' :
            #print('Ping Pong!')
            playsound("chime.wav")

if __name__ == '__main__':
    ##print(len(sys.argv))
    if (len(sys.argv) != 4):
        print("Usage: {} <id> <server ip> <server port>".format(
            sys.argv[0]))
        sys.exit(1)

    sid = sys.argv[1]
    serverip = sys.argv[2]
    serverport = sys.argv[3]
    server = (serverip, int(serverport))

    while True :
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.connect(server)
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            print('serverとの接続に失敗しました。 : %s:%s' % (serverip, serverport))
            continue

        try:
            data = soc.recv(4096).decode()
            print(str(data))
            cmd = str(data.rstrip())
            line = 'id;%s' % sid
            soc.send(line.encode('utf-8'))
        except:
            print('サーバーとの通信に失敗しました。再接続します :', datetime.now())
            continue
        loop(soc)
        soc.close()
        print('サーバーとの通信に失敗しました。再接続します :', datetime.now())