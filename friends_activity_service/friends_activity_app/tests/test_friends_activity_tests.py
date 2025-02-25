import asyncio
import random
from datetime import timedelta

import jwt
import pytest
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from friends_activity_app.asgi import application


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
        await asyncio.sleep(0.5)

        try:
            # communicator_2 は 1 回だけ受信
            response_from_second_client = await communicator_2.receive_json_from(
                timeout=1
            )
            assert user_id in response_from_second_client["current_users"]
            assert user_id_2 in response_from_second_client["current_users"]

            # communicator は複数回受信して最新のユーザーリストを取得
            received_users = set()

            for _ in range(2):  # 2回受信を試みる
                response_from_first_client = await communicator.receive_json_from(
                    timeout=1
                )
                received_users.update(response_from_first_client["current_users"])

                if user_id in received_users and user_id_2 in received_users:
                    break  # 期待するデータを受け取ったらループを抜ける

            assert user_id in received_users
            assert user_id_2 in received_users

        finally:
            # 接続解除
            await communicator.disconnect()
            await communicator_2.disconnect()

    async def test_websocket_user_logout_broadcasts_to_others(self):
        """1人がログアウトしたとき、他のユーザーに通知されるかテスト"""
        user_id_1 = str(random.randint(1, 1000))
        user_id_2 = str(random.randint(1, 1000))

        access_token_1 = self.create_jwt_for_user(user_id_1)
        access_token_2 = self.create_jwt_for_user(user_id_2)

        url = "/friends/online"

        communicator_1 = WebsocketCommunicator(application, url)
        communicator_1.scope["cookies"] = {"access_token": access_token_1}

        communicator_2 = WebsocketCommunicator(application, url)
        communicator_2.scope["cookies"] = {"access_token": access_token_2}

        connected_1, _ = await communicator_1.connect()
        connected_2, _ = await communicator_2.connect()
        assert connected_1
        assert connected_2

        await asyncio.sleep(0.5)

        # ユーザーリストを受信
        await communicator_1.receive_json_from()
        await communicator_2.receive_json_from()

        # 1人目のユーザーを切断
        await communicator_1.disconnect()

        # 2人目のクライアントが更新情報を受信するか確認
        response_from_second_client = await communicator_2.receive_json_from(timeout=1)
        assert response_from_second_client["status"] == "User removed"
        assert response_from_second_client["user_id"] == user_id_1
        assert user_id_1 not in response_from_second_client["current_users"]
        assert user_id_2 in response_from_second_client["current_users"]

        await communicator_2.disconnect()

    async def test_websocket_multiple_sessions_logout(self):
        """同じ user_id で複数接続し、1つを切断した際に user_list に残っているか確認"""
        user_id = str(random.randint(1, 1000))
        access_token = self.create_jwt_for_user(user_id)

        url = "/friends/online"

        communicator_1 = WebsocketCommunicator(application, url)
        communicator_1.scope["cookies"] = {"access_token": access_token}

        communicator_2 = WebsocketCommunicator(application, url)
        communicator_2.scope["cookies"] = {"access_token": access_token}

        connected_1, _ = await communicator_1.connect()
        connected_2, _ = await communicator_2.connect()
        assert connected_1
        assert connected_2

        await asyncio.sleep(0.5)

        # 初期ユーザーリストを受信
        await communicator_1.receive_json_from()
        await communicator_2.receive_json_from()

        # 1つのセッションを切断
        await communicator_1.disconnect()

        # まだ `user_id` がリストに残っていることを確認
        response_from_second_client = await communicator_2.receive_json_from(timeout=1)
        assert user_id in response_from_second_client["current_users"]

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

    async def test_websocket_without_jwt(self):
        url = "/friends/online/"
        communicator = WebsocketCommunicator(application, url)

        connected, _ = await communicator.connect()
        # JWTがないため、接続が確立されないはず
        assert not connected
