import jwt
import pyotp
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from auth_app.models import CustomUser
from auth_app.services.jwt_service import generate_signed_jwt

class UpdateEmailViewTest(TestCase):
    """
    UpdateEmailView のテスト
    """

    def setUp(self):
        """
        テスト前の初期セットアップ
        """
        self.client = APIClient()

        # テスト用ユーザ作成
        self.user = CustomUser.objects.create_user(
            user_id="test-user-123",
            email="old@example.com",
            secret_key=pyotp.random_base32(),
            hashed_password=make_password("securepassword"),
        )

        # Vault ベースの署名付き JWT を発行
        self.token = generate_signed_jwt(self.user.user_id)

        self.client.cookies["access_token"] = self.token

        self.url = reverse("update_email")

    def test_update_email_success(self):
        """
        正常にメールアドレスを更新できることを確認
        """
        response = self.client.put(
            self.url, {"email": "new@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Email updated successfully.")

        # DB の値が更新されているか確認
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new@example.com")

    def test_update_email_missing(self):
        """
        email がリクエストボディに存在しない場合 400 エラー
        """
        response = self.client.put(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("This field is required.", response.json()["error"])

    def test_update_email_invalid_format(self):
        """
        不正なフォーマットのメールアドレスを指定した場合 400 エラー
        """
        response = self.client.put(self.url, {"email": "invalid-email"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Enter a valid email address.", response.json()["error"])

    def test_update_email_conflict(self):
        """
        既に存在するメールアドレスを指定した場合 409 エラー
        """
        # 競合する別のユーザを作成
        CustomUser.objects.create_user(
            user_id="other-user-456",
            email="existing@example.com",
            secret_key=pyotp.random_base32(),
            hashed_password=make_password("securepassword"),
        )

        response = self.client.put(
            self.url, {"email": "existing@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["error"], "This email address is already in use."
        )

    def test_update_email_unauthorized(self):
        """
        Cookie に JWT が設定されていない場合 401 エラー
        """
        self.client.cookies.clear()
        response = self.client.put(
            self.url, {"email": "new@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Access token missing")
