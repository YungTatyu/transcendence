from datetime import timedelta
import unittest
from unittest.mock import MagicMock, patch

from channels.testing import WebsocketCommunicator
import pytest
from channels.generic.websocket import WebsocketConsumer
import jwt

from game_app.asgi import application
from core.match_manager import MatchManager
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
        self.players = [1, 2]
        self.create_match(self.match_id, self.players)
        self.is_default = default_player
        if default_player:
            self.player1, self.player1_connected = await self.create_communicator(
                self.match_id, self.players[0]
            )
            self.player2, self.player2_connected = await self.create_communicator(
                self.match_id, self.players[1]
            )
        GameController.GAME_TIME_SEC = 1

    async def teardown(self):
        if self.is_default:
            await self.player1.disconnect()
            await self.player2.disconnect()

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
        return communicator, connected

    async def test_establish_ws_connection(self):
        await self.setup()
        assert self.player1_connected is True
        assert self.player2_connected is True
        await self.teardown()
