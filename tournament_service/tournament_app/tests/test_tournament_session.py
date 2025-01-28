from django.test import TestCase

from tournament_app.utils.tournament_session import TournamentSession as TS


class TournamentSessionTest(TestCase):
    def setUp(self):
        TS.clear()

    def test_register(self):
        user_ids_1 = [1, 2]
        user_ids_2 = [11, 22, 33]
        TS.register(1, user_ids_1)
        TS.register(2, user_ids_2)
        self.assertEqual(user_ids_1, TS.search(1).user_ids)
        self.assertEqual(user_ids_2, TS.search(2).user_ids)

    def test_register_same_id(self):
        user_ids_1 = [1, 2, 3]
        user_ids_2 = [11, 22, 33]
        self.assertIsNotNone(TS.register(1, user_ids_1))
        self.assertIsNone(TS.register(1, user_ids_2))
        self.assertEqual(user_ids_1, TS.search(1).user_ids)

    def test_search_not_exist_id(self):
        user_ids = [1, 2, 3]
        TS.register(1, user_ids)
        self.assertIsNotNone(TS.search(1))
        self.assertIsNone(TS.search(2))

    def test_delete(self):
        user_ids = [1, 2, 3]
        self.assertFalse(TS.delete(1))
        TS.register(1, user_ids)
        self.assertTrue(TS.delete(1))
        self.assertFalse(TS.delete(1))

    def test_round(self):
        user_ids = [1, 2, 3]
        tournament_session = TS.register(1, user_ids)
        self.assertEqual(1, tournament_session.current_round)
        self.assertEqual(2, tournament_session.next_round())
        self.assertEqual(3, tournament_session.next_round())
        self.assertEqual(3, tournament_session.current_round)
