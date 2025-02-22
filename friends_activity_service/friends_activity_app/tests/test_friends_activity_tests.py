import random
from datetime import timedelta

import jwt
import pytest
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from friends_activity_app.asgi import application
import asyncio


@pytest.mark.asyncio
class TestLoggedInUsersConsumer(TestCase):
    async def test_websocket_connect_and_send_message(self):
        # ランダムなuser_idを生成
        user_id = str(random.randint(1, 1000))

        # JWTの発行（適宜変更）
        access_token = self.create_jwt_for_user(user_id)

        # WebSocket URL
        url = "/friends/online"

        # WebSocket接続
        communicator = WebsocketCommunicator(application, url)
        communicator.scope["cookies"] = {"access_token": access_token}

        # WebSocket接続を試みる
        connected, subprotocol = await communicator.connect()
        assert connected

        # ユーザーがリストに追加されることを確認
        response = await communicator.receive_json_from()
        assert response["status"] == "User added"
        assert response["user_id"] == user_id

        # 接続解除
        await communicator.disconnect()

    async def test_multiple_websocket_connect_and_send_message(self):
        # ランダムな user_id を生成
        user_id = str(random.randint(1, 1000))
        user_id_2 = str(random.randint(1, 1000))

        # JWT の発行
        access_token = self.create_jwt_for_user(user_id)
        access_token_2 = self.create_jwt_for_user(user_id_2)

        # WebSocket URL
        url = "/friends/online"

        # WebSocket接続
        communicator = WebsocketCommunicator(application, url)
        communicator.scope["cookies"] = {"access_token": access_token}
        
        communicator_2 = WebsocketCommunicator(application, url)
        communicator_2.scope["cookies"] = {"access_token": access_token_2}

        # WebSocket接続を試みる
        connected, _ = await communicator.connect()
        assert connected

        connected_2, _ = await communicator_2.connect()
        assert connected_2

        # サーバーのブロードキャストを待つ
        await asyncio.sleep(0.1)

        try:
            response_from_first_client = await communicator.receive_json_from(timeout=1)
            response_from_second_client = await communicator_2.receive_json_from(timeout=1)

            assert user_id in response_from_first_client["current_users"]
            assert user_id_2 in response_from_first_client["current_users"]
            assert user_id in response_from_second_client["current_users"]
            assert user_id_2 in response_from_second_client["current_users"]
        finally:
            # 接続解除
            await communicator.disconnect()
            await communicator_2.disconnect()


    def create_jwt_for_user(self, user_id):
        # JWTを生成するロジック
        payload = {
            "user_id": user_id,
            "exp": timedelta(days=1).total_seconds(),
            "iat": timedelta(days=0).total_seconds(),
        }
        secret_key = "your_secret_key"
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    async def test_websocket_invalid_jwt(self):
        # 無効なJWTを利用して接続を試みる
        invalid_token = "invalid_token"
        url = "/friends/online/"
        communicator = WebsocketCommunicator(application, url)
        communicator.scope["cookies"] = {"access_token": invalid_token}

        connected, _ = await communicator.connect()
        # JWTが無効なため、接続が確立されないはず
        assert not connected
