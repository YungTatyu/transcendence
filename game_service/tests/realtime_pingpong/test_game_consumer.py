import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from core.match_manager import MatchManager
from realtime_pingpong.consumers import GameConsumer


class TestGameController(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        MatchManager.remove_match = MagicMock(return_value=None)
        self.patcher = patch(
            "channels.layers.get_channel_layer", return_value=MagicMock()
        )
        self.mock_get_channel_layer = self.patcher.start()
        self.mock_channel_layer = self.mock_get_channel_layer.return_value
        self.result = {
            "matchId": 1,
            "results": [
                {"userId": 1, "score": 2},
                {"userId": 2, "score": 6},
            ],
        }

    def tearDown(self):
        self.patcher.stop()

    async def test_finish_game(self):
        await GameConsumer.finish_game(self.result, "1")
        MatchManager.remove_match.assert_called_once_with(1)
