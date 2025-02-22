import json

from channels.generic.websocket import AsyncWebsocketConsumer


class LoggedInUsersConsumer(AsyncWebsocketConsumer):
    # ユーザーリストをメモリ内で管理
    user_list = []
    group_name = "logged_in_users"

    async def connect(self):
        self.user_id = self.scope.get("user_id")
        if not self.user_id:
            await self.close()
            return

        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.add_user_to_list()

    async def disconnect(self, close_code):
        await self.remove_user_from_list()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def add_user_to_list(self):
        self.user_list.append(self.user_id)
        await self.broadcast_user_list("User added")

    async def remove_user_from_list(self):
        self.user_list.remove(self.user_id)
        await self.broadcast_user_list("User removed")

    async def broadcast_user_list(self, status):
        current_users = list(set(self.user_list))
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_user_list",
                "status": status,
                "user_id": self.user_id,
                "current_users": current_users,
            },
        )

    async def send_user_list(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "status": event["status"],
                    "user_id": event["user_id"],
                    "current_users": event["current_users"],
                }
            )
        )
