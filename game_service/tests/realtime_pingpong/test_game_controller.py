import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta

from realtime_pingpong.game_controller import GameController
from core.pingpong import PingPong


class TestGameController(unittest.IsolatedAsyncioTestCase):
    """GameController のテスト"""

    def setUp(self):
        """テスト前のセットアップ"""
        self.controller = GameController()
        self.controller.GAME_TIME_SEC = 1

        # PingPong ゲームのモックを設定
        self.mock_game = MagicMock()
        self.mock_game.state = PingPong.GameState.READY_TO_START
        self.mock_game.left_player.id = 1
        self.mock_game.right_player.id = 2
        self.controller._GameController__game = self.mock_game  # プライベート変数に設定

        # PlayerManager のモック
        self.controller._GameController__player_manager = MagicMock()

    async def test_start_game(self):
        """ゲームを開始できるかのテスト"""
        self.controller.game_loop = MagicMock()
        with patch("asyncio.create_task", return_value=MagicMock()) as mock_create_task:
            self.controller.start_game("test_group")

            # ゲーム状態が IN_PROGRESS に変更される
            self.assertEqual(self.controller.game.state, PingPong.GameState.IN_PROGRESS)
            self.controller._GameController__player_manager.add_players.assert_called_once_with(
                [1, 2]
            )
            mock_create_task.assert_called_once()

    async def test_stop_game(self):
        """ゲームを停止できるかのテスト"""
        task_mock = MagicMock()
        self.controller._GameController__task = task_mock

        self.controller.stop_game()

        # タスクがキャンセルされ、Noneに設定される
        task_mock.cancel.assert_called_once()
        self.assertIsNone(self.controller._GameController__task)

    async def test_reconnect_event(self):
        """再接続イベントのテスト"""
        self.controller._GameController__announce_game_end_time = AsyncMock()

        await self.controller.reconnect_event("test_group", 1)

        # プレイヤーの再接続とタイマーのアナウンスが行われる
        self.controller._GameController__player_manager.reconnect_player.assert_called_once_with(
            1
        )
        self.controller._GameController__announce_game_end_time.assert_awaited_once_with(
            "test_group"
        )

    async def test_disconnect_event(self):
        """切断イベントのテスト"""
        self.controller.disconnect_event(1)

        # プレイヤーの切断が行われる
        self.controller._GameController__player_manager.disconnect_player.assert_called_once_with(
            1
        )

    async def test_game_loop(self):
        """ゲームループのテスト"""
        self.mock_game.is_match_over.return_value = True

        with patch(
            "realtime_pingpong.consumers.GameConsumer.group_send",
            new_callable=AsyncMock,
        ) as mock_group_send:
            await self.controller.game_loop("test_group")

            # メッセージが送信され、ゲーム状態がGAME_OVERになる
            mock_group_send.assert_called()
            self.assertEqual(self.controller.game.state, PingPong.GameState.GAME_OVER)
