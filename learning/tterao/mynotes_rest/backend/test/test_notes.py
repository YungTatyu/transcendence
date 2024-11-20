from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class NoteCreateTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.create_url = reverse("note_create")  # URL名でリバース解決

    def test_create_note_success(self):
        title = "Test Note"
        content = "This is a test note."
        data = {"title": title, "content": content}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], title)
        self.assertEqual(response.data["content"], content)

    def test_create_note_failure_unauthenticated(self):
        self.client.credentials()  # トークンを削除
        data = {"title": "Test Note", "content": "This is a test note."}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note_failure_empty_title(self):
        data = {"title": "", "content": "This is a test note."}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_note_failure_empty_content(self):
        data = {"title": "title", "content": ""}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NoteDeleteTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # ノート作成用URLの取得
        self.create_url = reverse("note_create")  # URL名でリバース解決

        self.note_data = {"title": "Test Note", "content": "This is a test note."}
        response = self.client.post(self.create_url, self.note_data)
        self.note_id = response.data["id"]  # 作成されたノートのIDを取得

        self.delete_url = reverse(
            "note_delete", kwargs={"id": self.note_id}
        )  # URL名とkwargsでリバース解決

    def test_delete_note_success(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_note_failure_unauthenticated(self):
        # トークンを削除して認証を無効化
        self.client.credentials()

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_note_failure_invalid_id(self):
        response = self.client.delete(reverse("note_delete", kwargs={"id": 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_failure_invalid_user(self):
        User = get_user_model()
        new_user = User.objects.create_user(username="new", password="new")

        new_token = Token.objects.create(user=new_user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + new_token.key)

        # 作成したノートの削除を試みる
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
