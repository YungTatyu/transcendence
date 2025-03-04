import unittest
from unittest.mock import MagicMock, patch

from core.match_manager import MatchManager
from realtime_pingpong.consumers import GameConsumer


class TestGameConsumer(unittest.IsolatedAsyncioTestCase):
    @patch("channels.layers.get_channel_layer", return_value=MagicMock())
    async def test_finish_game(self, mock_get_channel_layer):
        MatchManager.remove_match = MagicMock(return_value=None)

        await GameConsumer.finish_game(
            {
                "matchId": 1,
                "results": [
                    {"userId": 1, "score": 2},
                    {"userId": 2, "score": 6},
                ],
            },
            "1",
        )
        MatchManager.remove_match.assert_called_once_with(1)
