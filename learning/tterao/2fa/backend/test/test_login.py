from auth_otp.models import User, UserTwoFactorVerification
from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        UserTwoFactorVerification.objects.create(
            user=self.user, otp_secret="test_secret"
        )

    def test_login_user_already_in_otp_phase(self):
        response = self.client.post(
            reverse("auth/login/otp/generate/"),
            {"username": "test_user", "password": "test_password"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(
            response.content, {"error": "User with this username already in otp phase."}
        )

    @patch("django.contrib.auth.authenticate")
    def test_login_authentication_failure(self, mock_authenticate):
        # `authenticate`がNoneを返すようにモック
        mock_authenticate.return_value = None

        response = self.client.post(
            reverse("auth/login/otp/generate/"),
            {"username": "invalid_user", "password": "wrong_password"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content, {"error": "invalid username or password."}
        )
        mock_authenticate.assert_called_once_with(
            username="invalid_user", password="wrong_password"
        )
