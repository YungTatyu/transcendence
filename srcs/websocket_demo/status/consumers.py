import json
from channels.generic.websocket import AsyncWebsocketConsumer

# アクティブユーザー数を管理する変数
active_users = 0

class ActiveUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global active_users

        await self.accept()

        active_users += 1

        await self.channel_layer.group_add(
            "active_users",
            self.channel_name
        )

        await self.channel_layer.group_send(
            "active_users",
            {
                "type": "update_user_count",
                "count": active_users,
            }
        )

    async def disconnect(self, close_code):
        global active_users
        active_users -= 1

        await self.channel_layer.group_send(
            "active_users",
            {
                "type": "update_user_count",
                "count": active_users,
            }
        )

        await self.channel_layer.group_discard(
            "active_users",
            self.channel_name
        )

    async def update_user_count(self, event):
        # クライアントにユーザー数を送信
        count = event["count"]
        await self.send(text_data=json.dumps({
            "count": count
        }))
