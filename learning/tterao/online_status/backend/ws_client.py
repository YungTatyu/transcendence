#! /usr/bin/python3
import asyncio
import websockets


async def websocket_client():
    uri = "ws://localhost:8000/status/"
    async with websockets.connect(uri) as websocket:
        # メッセージを送信
        print("connected")
        await websocket.send('{"message": "Hello, WebSocket!"}')
        print("Sent: Hello, WebSocket!")

        # サーバーからのメッセージを受信
        response = await websocket.recv()
        print(f"Received: {response}")


# 実行
asyncio.run(websocket_client())
