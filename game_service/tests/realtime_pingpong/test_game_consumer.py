import asyncio
from datetime import timedelta
import unittest
from unittest.mock import MagicMock, patch

from channels.testing import WebsocketCommunicator
import pytest
from channels.generic.websocket import WebsocketConsumer
import jwt

from game_app.asgi import application
from core.match_manager import MatchManager
from realtime_pingpong import game_controller
from realtime_pingpong.consumers import GameConsumer
from realtime_pingpong.game_controller import GameController


# class TestGameConsumer(unittest.IsolatedAsyncioTestCase):
#     @patch("channels.layers.get_channel_layer", return_value=MagicMock())
#     async def test_finish_game(self, mock_get_channel_layer):
#         MatchManager.remove_match = MagicMock(return_value=None)
#
#         await GameConsumer.finish_game(
#             {
#                 "matchId": 1,
#                 "results": [
#                     {"userId": 1, "score": 2},
#                     {"userId": 2, "score": 6},
#                 ],
#             },
#             "1",
#         )
#         MatchManager.remove_match.assert_called_once_with(1)
#


@pytest.mark.asyncio
class TestGameConsumer:
    async def setup(self, default_player=True):
        MatchManager.delete_all_matches()
        self.match_id = 1
        self.player_ids = [1, 2]
        self.create_match(self.match_id, self.player_ids)
        self.is_default = default_player
        self.clients = list()
        if default_player:
            self.client1, self.client1_connected = await self.create_communicator(
                self.match_id, self.player_ids[0]
            )
            self.client2, self.client2_connected = await self.create_communicator(
                self.match_id, self.player_ids[1]
            )
        GameController.GAME_TIME_SEC = 1

    async def teardown(self):
        if self.is_default:
            await self.client1.disconnect()
            await self.client2.disconnect()
        self.clients.clear()
        match = MatchManager.get_match(self.match_id)
        if match is not None:
            game_controller = match[MatchManager.KEY_GAME_CONTROLLER]
            game_controller.stop_game()

    def create_jwt_for_user(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": timedelta(days=1).total_seconds(),
            "iat": timedelta(days=0).total_seconds(),
        }
        secret_key = "your_secret_key"
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    def create_match(self, match_id, users):
        MatchManager.create_match(match_id, users)

    async def create_communicator(self, match_id, user_id):
        communicator = WebsocketCommunicator(
            application, f"/games/ws/enter-room/{match_id}"
        )
        access_token = self.create_jwt_for_user(user_id)
        communicator.scope["cookies"] = {"access_token": access_token}
        connected, _ = await communicator.connect()
        if connected:
            self.clients.append(communicator)
        return communicator, connected

    def assert_endtime_message(self, actual):
        assert actual.get("message") == GameConsumer.MessageType.MSG_TIMER
        assert actual.get("end_time") is not None
        assert actual.get("type") == "game.message"

    def assert_game_message(self, actual, expect_left_id, expect_right_id):
        assert actual.get("message") == GameConsumer.MessageType.MSG_UPDATE
        assert actual.get("type") == "game.message"

        data = actual.get("data")
        assert data is not None
        state = data.get("state")
        assert state is not None

        ball = state.get("ball")
        assert ball is not None
        assert ball.get("x") is not None
        assert ball.get("y") is not None

        left_player = state.get("left_player")
        assert left_player is not None
        assert left_player.get("id") == expect_left_id
        assert left_player.get("y") is not None
        assert left_player.get("score") is not None

        right_player = state.get("right_player")
        assert right_player is not None
        assert right_player.get("id") == expect_right_id
        assert right_player.get("y") is not None
        assert right_player.get("score") is not None

    def assert_gameover_message(self, actual, player_ids):
        assert actual.get("message") == GameConsumer.MessageType.MSG_GAME_OVER
        assert actual.get("type") == "game.finish.message"
        assert actual.get("matchId") == self.match_id

        results = actual.get("results")
        assert results is not None
        for i, res in enumerate(results):
            assert res.get("userId") == player_ids[i]
            assert res.get("score") is not None

    async def receive_until(self, client, target_message):
        """
        欲しいメッセージタイプが来るまでloopする
        """
        while True:
            res = await client.receive_json_from()
            # updateの場合は一回receiveしたら次のメッセージのはず
            if target_message == GameConsumer.MessageType.MSG_UPDATE:
                return None
            if res.get("message") == target_message:
                return res

    async def test_establish_ws_connection(self):
        await self.setup()
        assert self.client1_connected is True
        assert self.client2_connected is True
        await self.teardown()

    async def test_ws_open_message(self):
        await self.setup()
        for client in self.clients:
            res = await client.receive_json_from()
            self.assert_endtime_message(res)
        await self.teardown()

    async def test_game_message(self):
        """
        game進行中のメッセージはgameが続いている限り送られるので、1秒間テストする
        """
        await self.setup()
        for client in self.clients:
            await self.receive_until(client, GameConsumer.MessageType.MSG_UPDATE)

        start_time = asyncio.get_running_loop().time()
        # 1秒間game messageをテストする
        while (asyncio.get_running_loop().time() - start_time) < 1:
            for client in self.clients:
                res = await client.receive_json_from()
                self.assert_game_message(res, self.player_ids[0], self.player_ids[1])
        await self.teardown()

    async def test_gameover_message(self):
        await self.setup()
        responses = []
        for client in self.clients:
            responses.append(
                await self.receive_until(client, GameConsumer.MessageType.MSG_GAME_OVER)
            )
        for res in responses:
            self.assert_gameover_message(res, self.player_ids)
        await self.teardown()
