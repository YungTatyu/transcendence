#! /usr/bin/python3
import json
import websocket
import threading  # 別スレッドで標準入力を待機するために使用
import sys  # 標準入力を扱うために使用

# WebSocket URLの設定
ROOM_NAME = "example_room"  # 適切なroom_nameに置き換えてください
WS_URL = f"ws://localhost:8000/ws/chat/{ROOM_NAME}/"


def on_message(ws, message):
    """サーバーからのメッセージを受信したときの処理"""
    data = json.loads(message)
    print(f"\n[サーバーからのメッセージ]: {data['message']}")


def on_error(ws, error):
    """エラーが発生したときの処理"""
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    """WebSocket接続が閉じたときの処理"""
    print("WebSocket connection closed")


def on_open(ws):
    """WebSocket接続が開いたときの処理"""
    print("WebSocket connection opened")

    def send_messages():
        """標準入力からメッセージを受け取り送信"""
        try:
            while True:
                message = input("\n[あなたのメッセージ]: ")  # 標準入力を取得
                ws.send(json.dumps({"message": message}))  # メッセージを送信
        except KeyboardInterrupt:
            print("\n終了します...")
            ws.close()

    # 標準入力を別スレッドで待機
    threading.Thread(target=send_messages, daemon=True).start()


# WebSocketの設定と実行
ws = websocket.WebSocketApp(
    WS_URL, on_message=on_message, on_error=on_error, on_close=on_close
)
ws.on_open = on_open

# WebSocketを永続的に実行
ws.run_forever()
