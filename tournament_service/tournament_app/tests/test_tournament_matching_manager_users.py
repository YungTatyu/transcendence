from django.test import TestCase
from tournament_app.utils.tournament_matching_manager import (
    TournamentMatchingManager as TMM,
)


class TournamentMatchingManagerUsersTest(TestCase):
    def setUp(self):
        """テスト毎にTournamentMatchingManagerを初期化"""
        TMM.clear_matching_wait_users()
        TMM.cancel_task()

    def test_add_users(self):
        self.assertEqual(0, len(TMM.get_matching_wait_users()))
        self.assertEqual(1, TMM.add_matching_wait_users(1, "1"))
        self.assertEqual(2, TMM.add_matching_wait_users(2, "2"))

    def test_add_same_user(self):
        """同じuser_idをaddしたら上書きされる"""
        user_id = 1
        TMM.add_matching_wait_users(user_id, "1")
        TMM.add_matching_wait_users(user_id, "2")
        user_id1_value = TMM.get_matching_wait_users()[user_id]
        self.assertEqual("2", user_id1_value)
        self.assertEqual(1, len(TMM.get_matching_wait_users()))

    def test_del_users(self):
        user1_id = 1
        user2_id = 2
        TMM.add_matching_wait_users(user1_id, "1")
        TMM.add_matching_wait_users(user2_id, "2")
        self.assertEqual(1, TMM.del_matching_wait_user(user1_id))
        self.assertEqual(0, TMM.del_matching_wait_user(user2_id))

    def test_del_not_exist_user(self):
        """存在しないユーザーを削除しても何も起こらない"""
        self.assertEqual(0, len(TMM.get_matching_wait_users()))
        self.assertEqual(0, TMM.del_matching_wait_user(10))

    def test_clear_users(self):
        TMM.add_matching_wait_users(1, "1")
        TMM.add_matching_wait_users(2, "2")
        self.assertEqual(2, len(TMM.get_matching_wait_users()))
        TMM.clear_matching_wait_users()
        self.assertEqual(0, len(TMM.get_matching_wait_users()))
