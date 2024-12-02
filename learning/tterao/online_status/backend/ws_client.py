#! /usr/bin/python3
import json
import asyncio
import websockets


# WebSocket サーバーのURL (Django Channels サーバーに置き換えてください)
WEBSOCKET_SERVER_URL = "ws://localhost:8000/status/"  # サーバーのエンドポイント


async def websocket_client():
    while True:
        try:
            # WebSocket サーバーに接続
            async with websockets.connect(WEBSOCKET_SERVER_URL) as websocket:
                print("Connected to WebSocket server.")

                # サーバーとの通信を処理
                while True:
                    # サーバーからのメッセージを受信
                    message = await websocket.recv()
                    data = json.loads(message)

                    # サーバーから受け取ったデータを表示
                    print("Received data:", data)

        except websockets.ConnectionClosed:
            print("Connection closed. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # 再接続までの待機時間

        except Exception as e:
            print(f"Error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # 再接続までの待機時間


# イベントループを開始
if __name__ == "__main__":
    asyncio.run(websocket_client())
