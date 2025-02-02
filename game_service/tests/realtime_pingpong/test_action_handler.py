import unittest
from unittest.mock import patch, MagicMock

from core.match_manager import MatchManager
from realtime_pingpong.consumers import ActionHandler


class ActionHandlerTestCase(unittest.TestCase):
    def setUp(self):
        # MatchManager.get_match をモックする
        patcher = patch("realtime_pingpong.consumers.MatchManager.get_match")
        self.mock_get_match = patcher.start()

        # モックされた match と game controller を準備
        self.mock_match = MagicMock()
        self.mock_match.match_id = 1
        self.mock_match.players = [1, 2]

        self.mock_game_controller = MagicMock()
        self.mock_game_controller.game = MagicMock()
        self.mock_game_controller.start_game = MagicMock(return_value=None)
        self.mock_game_controller.reconnect_event = MagicMock(return_value=None)

        self.mock_get_match.return_value = {
            MatchManager.KEY_MATCH: self.mock_match,
            MatchManager.KEY_GAME_CONTROLLER: self.mock_game_controller,
        }

        # テストが終了した後でモックを停止する
        self.addCleanup(patcher.stop)

    def test_handle_new_connection_success(self):
        result, status_code = ActionHandler.handle_new_connection(1, 1)

        self.mock_game_controller.game.add_player.assert_called_once()
        self.assertTrue(result)
        self.assertEqual(status_code, 200)

    def test_handle_new_connection_match_not_registered(self):
        self.mock_get_match.return_value = None
        result, status_code = ActionHandler.handle_new_connection(1, 1)

        self.assertFalse(result)
        self.assertEqual(status_code, 1003)

    def test_handle_new_connection_invalid_player(self):
        result, status_code = ActionHandler.handle_new_connection(1, 3)

        self.assertFalse(result)
        self.assertEqual(status_code, 1008)

    def test_handle_new_connection_missing_match_id(self):
        result, status_code = ActionHandler.handle_new_connection(None, 1)

        self.assertFalse(result)
        self.assertEqual(status_code, 1008)

    def test_handle_new_connection_missing_user_id(self):
        result, status_code = ActionHandler.handle_new_connection(1, None)

        self.assertFalse(result)
        self.assertEqual(status_code, 1008)
