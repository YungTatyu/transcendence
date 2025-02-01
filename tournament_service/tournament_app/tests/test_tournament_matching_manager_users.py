from django.test import TestCase

from tournament_app.utils.tournament_matching_manager import (
    TournamentMatchingManager as Tmm,
)


class TournamentMatchingManagerUsersTest(TestCase):
    def setUp(self):
        """テスト毎にTournamentMatchingManagerを初期化"""
        Tmm.clear_waiting_users()
        Tmm.cancel_task()

    def test_add_users(self):
        self.assertEqual(0, len(Tmm.get_waiting_users()))
        self.assertEqual(1, Tmm.add_user(1, "1"))
        self.assertEqual(2, Tmm.add_user(2, "2"))

    def test_add_same_user(self):
        """同じuser_idをaddしたら上書きされる"""
        user_id = 1
        Tmm.add_user(user_id, "1")
        Tmm.add_user(user_id, "2")
        user_id1_value = Tmm.get_waiting_users()[user_id]
        self.assertEqual("2", user_id1_value)
        self.assertEqual(1, len(Tmm.get_waiting_users()))

    def test_del_users(self):
        user1_id = 1
        user2_id = 2
        Tmm.add_user(user1_id, "1")
        Tmm.add_user(user2_id, "2")
        self.assertEqual(1, Tmm.del_user(user1_id))
        self.assertEqual(0, Tmm.del_user(user2_id))

    def test_del_not_exist_user(self):
        """存在しないユーザーを削除しても何も起こらない"""
        self.assertEqual(0, len(Tmm.get_waiting_users()))
        self.assertEqual(0, Tmm.del_user(10))

    def test_clear_users(self):
        Tmm.add_user(1, "1")
        Tmm.add_user(2, "2")
        self.assertEqual(2, len(Tmm.get_waiting_users()))
        Tmm.clear_waiting_users()
        self.assertEqual(0, len(Tmm.get_waiting_users()))
