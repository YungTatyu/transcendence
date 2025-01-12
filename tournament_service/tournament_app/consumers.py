import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # WebSocket接続時に呼び出される
        print("WebSocket connection established")

        await self.accept()
        # クライアントに接続確認のメッセージを送信
        await self.send(text_data=json.dumps({"message": "Connection established!"}))

    async def disconnect(self, close_code):
        # WebSocket切断時に呼び出される
        print("WebSocket connection closed", close_code)

    async def receive(self, text_data):
        # クライアントからメッセージを受け取る
        print(f"Received message: {text_data}")

        # メッセージを受け取った後、クライアントに同じメッセージを送り返す
        await self.send(text_data=json.dumps({"message": text_data}))
