from datetime import timedelta

import jwt
import pytest
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from config.asgi import application
from match_app.utils.quick_play_matching_manager import QuickPlayMatchingManager
import sys

PATH_MATCHING = "/matches/ws/enter-room"


@pytest.mark.asyncio
class TestQuickPlayConsumer(TestCase):
    def setUp(self):
        QuickPlayMatchingManager.clear_waiting_users()

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

    async def create_communicator(self, user_id: int, expect_connected=True):
        """JWTをCookieに含んでWebSocketコネクションを作成"""
        access_token = self.create_jwt_for_user(user_id)
        communicator = WebsocketCommunicator(application, PATH_MATCHING)
        communicator.scope["cookies"] = {"access_token": access_token}
        connected, _ = await communicator.connect()
        assert connected == expect_connected
        return communicator

    @pytest.mark.asyncio(loop_scope="function")
    async def test_websocket_connect(self):
        user_id = 1

        communicator = await self.create_communicator(user_id)

        # 接続解除
        await communicator.disconnect()

    @pytest.mark.asyncio(loop_scope="function")
    async def test_has_not_jwt(self):
        """コネクション確立時にJWTを含まないケースはコネクションが確立できない"""
        communicator = WebsocketCommunicator(application, PATH_MATCHING)
        connected, _ = await communicator.connect()
        assert not connected

    @pytest.mark.asyncio(loop_scope="function")
    async def test_enter_room_same_user(self):
        """同一ユーザーがマッチングルームに入った場合、コネクションが確立できない"""
        user_id = 1

        communicator = await self.create_communicator(user_id)
        await self.create_communicator(user_id, expect_connected=False)
        print(communicator, file=sys.stderr)

        await communicator.disconnect()
