from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.match_manager import MatchManager
from core.serializers import GameSerializer


class GameViewsTestCase(APITestCase):
    def setUp(self):
        # 各テストメソッドが実行される前に呼び出される初期化メソッド
        self.url = reverse("games")

        MatchManager.delete_all_matches()

    def create_match(self, data):
        return self.client.post(self.url, data, format="json")

    def test_create_match_with_two_players(self):
        data = {GameSerializer.KEY_MATCH_ID: 1, GameSerializer.KEY_USERS: [1, 2]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(MatchManager.get_match(1))

    def test_create_match_with_one_player(self):
        data = {GameSerializer.KEY_MATCH_ID: 2, GameSerializer.KEY_USERS: [1]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(MatchManager.get_match(2))

    def test_create_match_with_three_players(self):
        data = {GameSerializer.KEY_MATCH_ID: 3, GameSerializer.KEY_USERS: [1, 2, 3]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(MatchManager.get_match(3))

    def test_create_match_with_no_players(self):
        data = {GameSerializer.KEY_MATCH_ID: 1, GameSerializer.KEY_USERS: []}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(MatchManager.get_match(1))

    def test_create_match_with_no_matchid(self):
        data = {GameSerializer.KEY_MATCH_ID: "", GameSerializer.KEY_USERS: [1, 2]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_match_with_no_matchid(self):
        data = {"match_id": 1, GameSerializer.KEY_USERS: [1, 2]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(MatchManager.get_match(1))

    def test_create_match_with_no_userid_list(self):
        data = {GameSerializer.KEY_MATCH_ID: 1, "users": [1, 2]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(MatchManager.get_match(1))

    def test_create_match_with_duplicated_match(self):
        self.create_match(
            {GameSerializer.KEY_MATCH_ID: 5, GameSerializer.KEY_USERS: [1, 2]}
        )
        match_before = MatchManager.get_match(5)

        # 同じmatchを登録
        response = self.create_match(
            {GameSerializer.KEY_MATCH_ID: 5, GameSerializer.KEY_USERS: [3, 4]}
        )
        match_after = MatchManager.get_match(5)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(match_before, match_after)
