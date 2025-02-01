import unittest
from unittest.mock import patch, MagicMock

from core.match_manager import MatchManager


# class ActionHandlerTestCase(unittest.TestCase):
#     def setUp(self):
#         # MatchManager.get_match をモックする
#         patcher = patch("realtime_pingpong.consumers.MatchManager.get_match")
#         self.mock_get_match = patcher.start()
#
#         # モックされた match と game controller を準備
#         self.mock_match = MagicMock()
#         self.mock_match.players = {"user1": True}
#         self.mock_get_match.return_value = {
#             MatchManager.KEY_MATCH: self.mock_match,
#             MatchManager.KEY_GAME_CONTROLLER: MagicMock(),
#         }
#
#         # テストが終了した後でモックを停止する
#         self.addCleanup(patcher.stop)
#
#     @patch("realtime_pingpong.consumers.MatchManager.get_match")
#     def test_handle_new_connection_success(self, mock_get_match):
#         # モックを使ってMatchManagerの戻り値を設定
#         mock_match = MagicMock()
#         mock_match.players = {"user1": True}
#         mock_get_match.return_value = {
#             MatchManager.KEY_MATCH: mock_match,
#             MatchManager.KEY_GAME_CONTROLLER: MagicMock(),
#         }
#
#         # メソッド呼び出し
#         result, status_code = ActionHandler.handle_new_connection("match1", "user1")
#
#         # 結果の検証
#         self.assertTrue(result)
#         self.assertEqual(status_code, 200)
