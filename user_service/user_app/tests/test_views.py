from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user_app.models import User

class UserAPITest(APITestCase):
    def setUp(self):
        """テスト用のデータ作成"""
        self.user = User.objects.create(username="testuser", avatar_path="/uploads/test.png")
        self.url = reverse("users")  # URLConf の名前

    def test_get_user_by_username(self):
        """GET /users?username=testuser が正しく動作するか"""
        response = self.client.get(self.url, {"username": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_get_user_not_found(self):
        """存在しないユーザーを検索すると 404 になるか"""
        response = self.client.get(self.url, {"username": "unknown"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_create_user(self):
        """POST /users で新しいユーザーを作成"""
        response = self.client.post(self.url, {"username": "newuser"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())
