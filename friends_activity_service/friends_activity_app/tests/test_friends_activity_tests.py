import json
import random
import pytest
from channels.testing import WebsocketCommunicator
from friends_activity_app.consumers import LoggedInUsersConsumer
from datetime import timedelta
import jwt
from django.test import TestCase
import asyncio

@pytest.mark.asyncio
class TestLoggedInUsersConsumer(TestCase):

    async def test_websocket_connect_and_send_message(self):
        # ランダムなuser_idを生成
        user_id = str(random.randint(1, 1000))

        # JWTの発行（適宜変更）
        access_token = self.create_jwt_for_user(user_id)

        # WebSocket URL
        url = 'ws://localhost:8000/ws/logged-in-users/'

        # WebSocket接続
        communicator = WebsocketCommunicator(LoggedInUsersConsumer.as_asgi(), url)

        # JWTをクッキーに設定して接続
        communicator.scope['cookies'] = {'access_token': access_token}

        # WebSocket接続を試みる
        connected, subprotocol = await communicator.connect()
        assert connected

        # ユーザーがリストに追加されることを確認
        response = await communicator.receive_json_from()
        assert response['status'] == 'User added'
        assert response['user_id'] == user_id

        # 送信されるログインユーザーリストを確認
        response = await communicator.receive_json_from()
        assert response['status'] == 'Current logged in users'
        assert 'current_users' in response

        # 接続解除
        await communicator.disconnect()

    def create_jwt_for_user(self, user_id):
        # JWTを生成するロジック
        payload = {
            'user_id': user_id,
            'exp': timedelta(days=1).total_seconds(),
            'iat': timedelta(days=0).total_seconds(),
        }
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
