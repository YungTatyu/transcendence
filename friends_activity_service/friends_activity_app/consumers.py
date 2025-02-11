import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import random

class LoggedInUsersConsumer(AsyncWebsocketConsumer):
    # ユーザーリストをメモリ内で管理
    user_list = []

    async def connect(self):
        self.channel_name = self.channel_name  # チャネル名の一意性を保つ

        # 一時的にランダムな数字をidとする
        self.user_id = str(random.randint(1, 1000))

        # WebSocket接続の確立
        await self.accept()

        # ユーザーをリストに追加
        await self.add_user_to_list()

        # 定期的にログインユーザーリストを送信
        await self.send_logged_in_users_periodically()

    async def disconnect(self, close_code):
        # WebSocket接続が切断されたときにユーザーをリストから削除
        await self.remove_user_from_list()

    async def receive(self, text_data):
        pass

    async def add_user_to_list(self):
        # ユーザーリストに追加
        self.user_list.append(self.user_id)

        # ユーザーリストをクライアントに送信
        await self.send(text_data=json.dumps({
            'status': 'User added',
            'user_id': self.user_id,
            'current_users': self.user_list,
        }))

    async def remove_user_from_list(self):
        # ユーザーリストから削除
        if self.user_id in self.user_list:
            self.user_list.remove(self.user_id)

        await self.send(text_data=json.dumps({
            'status': 'User removed',
            'user_id': self.user_id,
            'current_users': self.user_list,
        }))

    async def send_logged_in_users_periodically(self):
        while True:
            await asyncio.sleep(5)  # 5秒ごとに送信
            await self.send(text_data=json.dumps({
                'status': 'Current logged in users',
                'current_users': self.user_list,
            }))
