import json
from channels.auth import login
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        user = self.user
        # login the user to this session.
        await login(self.scope, user)
        # save the session (if the session backend does not access the db you can use `sync_to_async`)
        await database_sync_to_async(self.scope["session"].save)()
        await self.send(text_data=json.dumps({"message": "message"}))
