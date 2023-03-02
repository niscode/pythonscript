## 事前にライブラリをインポート
- `pip install -r requirements.txt`

#### 以下のpythonモジュールを使用します。3系です。
    - selenium
    - websocket-client
    - pyopenssl
    - urllib3
    - requests
    - bs4
    - evdev

## 第2期 Jetson-Nano 用にカスタマイズ
#### websocket経由でCAPFとの接続が可能になりました。〔2023.3.1〕

    launch_ws.sh を実行すると webagent.py が起動し、
    ペアとなるSOTA / ペアとなるOP を指定し、CAPFに接続します。

1. <strong>コマンド受信機能</strong><br>
    websocket経由でCAPFからのコマンドを受け取ります。

1. <strong>CAPFコマンドの中継機能</strong><br>
    TCP-socket 経由でペアのSOTAに対しコマンドを送ります。<br>
    主にCAPFから受け取ったコマンドを SOTAに中継するための機能です。

2. <strong>USBボタン信号の送信機能</strong><br>
    接続されたUSBボタンが押下された際、<br>
    指定されたペアのOP宛の指令値として、<br>
    websocket 経由でCAPFにコマンドを発行します。
