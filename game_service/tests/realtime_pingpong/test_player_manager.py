import unittest

from realtime_pingpong.game_controller import PlayerManager


class TestPlayerManager(unittest.TestCase):
    def setUp(self):
        """テストごとに新しい PlayerManager インスタンスを作成"""
        self.manager = PlayerManager()

    def test_add_players(self):
        self.manager.add_players([1, 2])
        self.assertTrue(self.manager.is_active(1))
        self.assertTrue(self.manager.is_active(2))

    def test_reconnect_player(self):
        """切断後のプレイヤーを再接続するとアクティブになることを確認"""
        self.manager.add_players([1, 2])
        self.manager.disconnect_player(1)
        self.assertFalse(self.manager.is_active(1))

        self.manager.reconnect_player(1)
        self.assertTrue(self.manager.is_active(1))

    def test_disconnect_player(self):
        """プレイヤーが切断されると非アクティブになることを確認"""
        self.manager.add_players([1, 2])
        self.manager.disconnect_player(1)

        self.assertFalse(self.manager.is_active(1))
        self.assertTrue(self.manager.is_active(2))

    def test_has_active_players(self):
        """アクティブなプレイヤーがいるかどうかを確認"""
        self.manager.add_players([1, 2])
        self.assertTrue(self.manager.has_active_players())

        self.manager.disconnect_player(1)
        self.manager.disconnect_player(2)
        self.assertFalse(self.manager.has_active_players())
