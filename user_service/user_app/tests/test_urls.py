from django.test import SimpleTestCase
from django.urls import resolve, reverse

from user_app.views import UserView


class TestUrls(SimpleTestCase):
    def test_users_url_resolves(self):
        """エンドポイント /users が UserView にマッピングされているか"""
        url = reverse("users")
        self.assertEqual(resolve(url).func.view_class, UserView)
