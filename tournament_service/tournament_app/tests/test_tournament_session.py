import pytest
from django.test import TestCase

from tournament_app.utils.tournament_session import TournamentSession as Ts


@pytest.mark.usefixtures("create_match_records_mocker")
class TournamentSessionTest(TestCase):
    def setUp(self):
        Ts.clear()

    def test_register(self):
        user_ids_1 = [1, 2]
        user_ids_2 = [11, 22, 33]
        Ts.register(1, user_ids_1)
        Ts.register(2, user_ids_2)
        self.assertEqual(user_ids_1, Ts.search(1).user_ids)
        self.assertEqual(user_ids_2, Ts.search(2).user_ids)

    def test_register_same_id(self):
        user_ids_1 = [1, 2, 3]
        user_ids_2 = [11, 22, 33]
        self.assertIsNotNone(Ts.register(1, user_ids_1))
        self.assertIsNone(Ts.register(1, user_ids_2))
        self.assertEqual(user_ids_1, Ts.search(1).user_ids)

    def test_search_not_exist_id(self):
        user_ids = [1, 2, 3]
        Ts.register(1, user_ids)
        self.assertIsNotNone(Ts.search(1))
        self.assertIsNone(Ts.search(2))

    def test_delete(self):
        user_ids = [1, 2, 3]
        self.assertFalse(Ts.delete(1))
        Ts.register(1, user_ids)
        self.assertTrue(Ts.delete(1))
        self.assertFalse(Ts.delete(1))

    def test_round(self):
        user_ids = [1, 2, 3]
        tournament_session = Ts.register(1, user_ids)
        self.assertEqual(1, tournament_session.current_round)
        self.assertEqual(2, tournament_session.next_round())
        self.assertEqual(3, tournament_session.next_round())
        self.assertEqual(3, tournament_session.current_round)
