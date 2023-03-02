### 事前にライブラリをインポート
- `pip install -r requirements.txt`

#### 以下のpythonモジュールを使用します。3系です。
    - selenium
    - websocket-client
    - pyopenssl
    - urllib3
    - requests
    - bs4
    - evdev

### 第2期 Jetson-Nano 用にカスタマイズ
#### websocket経由でCAPFとの接続が可能です。

    launch_ws.sh を実行すると webagent.py が起動し、
    ペアとなるSOTA / ペアとなるOP を指定し、CAPFに接続します。

1. <strong>CAPFコマンドの中継機能</strong><br>
    CAPFからのコマンドを websocekt で受け取り、<br>
    ペアのSOTAに対し TCP-socket でコマンドを送ります。

2. <strong>USBボタン信号の送信機能</strong><br>
    接続されたUSBボタンが押下された際、<br>
    指定されたペアのOP宛の指令値として、<br>
    websocket 経由でCAPFにコマンドを発行します。

3. <strong>コマンド受信機能</strong><br>
    websocket経由でCAPFからのコマンドを受け取ります。