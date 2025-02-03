import unittest
from unittest.mock import AsyncMock, patch, MagicMock

from core.match_manager import MatchManager
from core.pingpong import PingPong
from realtime_pingpong.consumers import ActionHandler


class ActionHandlerTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # MatchManager.get_match をモックする
        patcher = patch("realtime_pingpong.consumers.MatchManager.get_match")
        self.mock_get_match = patcher.start()

        # モックされた match と game controller を準備
        self.mock_match = MagicMock()
        self.mock_match.match_id = 1
        self.mock_match.players = [1, 2]

        self.mock_game_controller = MagicMock()
        self.mock_game = MagicMock()
        self.mock_game_controller.game = self.mock_game
        self.mock_game_controller.start_game = MagicMock(return_value=None)
        self.mock_game_controller.reconnect_event = AsyncMock(return_value=None)
        self.mock_game_controller.disconnect_event = MagicMock(return_value=None)

        self.mock_get_match.return_value = {
            MatchManager.KEY_MATCH: self.mock_match,
            MatchManager.KEY_GAME_CONTROLLER: self.mock_game_controller,
        }

        # テストが終了した後でモックを停止する
        self.addCleanup(patcher.stop)

    def test_handle_new_connection_success(self):
        result, status_code = ActionHandler.handle_new_connection(1, 2)

        self.mock_game_controller.game.add_player.assert_called_once_with(2)
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

    def test_handle_player_action_success(self):
        ActionHandler.handle_player_action(
            {
                "type": ActionHandler.ACTION_PADDLE,
                "key": "KeyW",
                "userid": "1",
            },
            self.mock_game,
        )
        self.mock_game.player_action.assert_called_once_with(1, "KeyW")

    def test_handle_player_action_unknown_key(self):
        ActionHandler.handle_player_action(
            {
                "type": "test",
                "key": "KeyW",
                "userid": "1",
            },
            self.mock_game,
        )
        self.mock_game.player_action.assert_not_called()

    def test_handle_player_action_missing_key(self):
        ActionHandler.handle_player_action(
            {
                "key": "KeyW",
                "userid": "1",
            },
            self.mock_game,
        )
        self.mock_game.player_action.assert_not_called()

    def test_handle_player_action_invalid_userid(self):
        ActionHandler.handle_player_action(
            {
                "type": ActionHandler.ACTION_PADDLE,
                "key": "KeyW",
                "userid": "test",
            },
            self.mock_game,
        )
        self.mock_game.player_action.assert_not_called()

    async def test_handle_game_connection_start_game(self):
        self.mock_game.state = PingPong.GameState.READY_TO_START
        await ActionHandler.handle_game_connection(1, 2)
        self.mock_game_controller.start_game.assert_called_once_with(str(1))

    async def test_handle_game_connection_reconnect_event(self):
        self.mock_game.state = PingPong.GameState.IN_PROGRESS
        await ActionHandler.handle_game_connection(1, 2)
        self.mock_game_controller.reconnect_event.assert_called_once_with(str(1), 2)

    async def test_handle_disconnection_remove_match(self):
        with patch("core.match_manager.MatchManager.remove_match") as mock_remove_match:
            self.mock_game.state = PingPong.GameState.GAME_OVER
            ActionHandler.handle_disconnection(1, 2)
            mock_remove_match.assert_called_once_with(1)

    async def test_handle_disconnection_disconnect_event_in_progress(self):
        with patch("core.match_manager.MatchManager.remove_match") as mock_remove_match:
            self.mock_game.state = PingPong.GameState.IN_PROGRESS
            ActionHandler.handle_disconnection(1, 2)
            self.mock_game_controller.disconnect_event.assert_called_once_with(2)
            mock_remove_match.assert_not_called()

    async def test_handle_disconnection_disconnect_event_ready(self):
        with patch("core.match_manager.MatchManager.remove_match") as mock_remove_match:
            self.mock_game.state = PingPong.GameState.READY_TO_START
            ActionHandler.handle_disconnection(1, 2)
            self.mock_game_controller.disconnect_event.assert_called_once_with(2)
            mock_remove_match.assert_not_called()

    async def test_handle_disconnection_disconnect_waiting(self):
        with patch("core.match_manager.MatchManager.remove_match") as mock_remove_match:
            self.mock_game.state = PingPong.GameState.WAITING_FOR_SECOND_PLAYER
            ActionHandler.handle_disconnection(1, 2)
            self.mock_game_controller.disconnect_event.assert_called_once_with(2)
            mock_remove_match.assert_not_called()
