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
