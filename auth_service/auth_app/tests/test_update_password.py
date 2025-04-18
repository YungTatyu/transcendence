import pyotp
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from auth_app.models import CustomUser
from auth_app.services.jwt_service import generate_signed_jwt


class UpdatePasswordViewTest(TestCase):
    """
    UpdatePasswordView のテスト
    """

    def setUp(self):
        """
        テスト前の初期セットアップ
        """
        self.client = APIClient()

        # テスト用ユーザ作成
        self.user = CustomUser.objects.create_user(
            user_id="test-user-123",
            email="test@example.com",
            secret_key=pyotp.random_base32(),
            hashed_password=make_password("securepassword"),
        )

        # Vault ベースの署名付き JWT を発行
        self.token = generate_signed_jwt(self.user.user_id)

        self.client.cookies["access_token"] = self.token
        self.url = reverse("update_password")

    def test_update_password_success(self):
        """
        正常にパスワードを更新できることを確認
        """
        response = self.client.put(
            self.url,
            {"current_password": "securepassword", "new_password": "newsecurepassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Password updated successfully.")

        # DB の値が更新されているか確認
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword"))

    def test_update_password_wrong_current(self):
        """
        現在のパスワードが間違っている場合 400 エラー
        """
        response = self.client.put(
            self.url,
            {"current_password": "wrongpassword", "new_password": "newsecurepassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Current password is incorrect.", response.json()["error"])

    def test_update_password_missing_fields(self):
        """
        current_password または new_password がリクエストボディに存在しない場合 400 エラー
        """
        response = self.client.put(
            self.url,
            {"new_password": "newsecurepassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("This field is required.", response.json()["error"])

    def test_update_password_unauthorized(self):
        """
        Cookie に JWT が設定されていない場合 401 エラー
        """
        self.client.cookies.clear()
        response = self.client.put(
            self.url,
            {"current_password": "securepassword", "new_password": "newsecurepassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Access token missing")
