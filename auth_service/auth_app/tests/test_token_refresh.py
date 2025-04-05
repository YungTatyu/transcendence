from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import CustomUser
from auth_app.services.jwt_service import generate_signed_jwt
from auth_app.settings import REFRESH_TOKEN_EXPIRATION


class TokenRefreshTests(APITestCase):
    """
    /auth/token/refresh エンドポイントのテスト
    """

    def setUp(self):
        self.user_id = "99999"
        self.email = "refreshuser@example.com"
        self.password = "refreshpass"
        self.secret_key = "S3CR3TKEYFOROTP"
        self.user = CustomUser.objects.create_user(
            user_id=self.user_id,
            email=self.email,
            secret_key=self.secret_key,
            hashed_password=self.password,
        )
        self.url = reverse("token_refresh")

    def test_refresh_token_success(self):
        """
        正しい refresh token で新しい access token が発行される
        """
        refresh_token = generate_signed_jwt(str(self.user_id), REFRESH_TOKEN_EXPIRATION)

        response = self.client.post(self.url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("accessToken", response.data)
        self.assertIn("access_token", response.cookies)

    def test_refresh_token_missing(self):
        """
        refresh token が送信されていない場合 400 を返す
        """
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Refresh token is missing.")

    def test_refresh_token_invalid(self):
        """
        無効な refresh token の場合 401 を返す
        """
        response = self.client.post(self.url, {"refresh": "invalid.token.value"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Refresh token is missing or invalid.")
