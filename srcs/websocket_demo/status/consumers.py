import json
from channels.generic.websocket import AsyncWebsocketConsumer

# ユーザーステータスを管理する辞書
user_status = {}

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            "status_group",
            self.channel_name
        )

    async def disconnect(self, close_code):
        for username, status in user_status.items():
            if status["channel_name"] == self.channel_name:
                del user_status[username]
                await self.notify_status_update()
                break

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get("username")
        action = data.get("action")

        if username and action == "online":
            user_status[username] = {
                "status": "Online",
                "channel_name": self.channel_name,
            }
            await self.notify_status_update()

    async def notify_status_update(self):
        await self.channel_layer.group_send(
            "status_group",
            {
                "type": "update_status",
                "user_status": user_status,
            }
        )

    async def update_status(self, event):
        await self.send(text_data=json.dumps({
            "user_status": event["user_status"]
        }))
