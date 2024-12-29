import json

from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "game"
        self.room_group_name = "game"
        # Join room group
        # awitはブロックするわけではない。処理を待つが待ってる間に他の処理を実行する
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            # self.room_group_name, {"type": "game.message", "message": message}
            self.room_group_name,
            {"type": "game.message"} | text_data_json,
        )

    # async_to_sync(self.channel_layer.group_send)の時にしてされたtypeがgame.messageのときにこの関数が呼ばれる
    async def game_message(self, event):
        print("event", event)
        message = event["message"]
        timer = event["timer"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
