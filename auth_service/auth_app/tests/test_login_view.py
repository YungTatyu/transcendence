from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import CustomUser
from auth_app.services.otp_service import OTPService
from django.urls import reverse
import uuid
import pyotp

class OTPAuthTests(APITestCase):
    """
    OTP 認証に関するテスト
    """

    def setUp(self):
        """
        テストデータの作成
        """
        self.user_id = "12345"  # ユニークな `user_id`
        self.username = "mockuser"
        self.email = "test@example.com"
        self.password = "securepassword"
        self.user = CustomUser.objects.create_user(
            user_id=self.user_id, email=self.email, password=self.password
        )

        # OTP 秘密鍵をユーザーに保存
        self.user.secret_key = pyotp.random_base32()
        self.user.save()

        # ログインエンドポイント
        self.login_url = reverse("otp-login")  # `/auth/otp/login/`
        self.verify_url = reverse("otp-login-verify")  # `/auth/otp/verify/`

    def test_login_success(self):
        """
        ✅ 正しい認証情報でログイン成功
        """
        response = self.client.post(self.login_url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Use the OTP generated by your authentication app to complete the login process.")

        # Cookie に `email` が保存されているか
        self.assertIn("email", response.cookies)

    def test_login_invalid_password(self):
        """
        ✅ 誤ったパスワードで認証できない
        """
        response = self.client.post(self.login_url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid email or password.")

    def test_login_missing_fields(self):
        """
        ✅ usernameまたはパスワードがない場合にエラー
        """
        response = self.client.post(self.login_url, {"password": self.password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.login_url, {"username": self.username})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_otp_verification_success(self):
        """
        ✅ 正しい OTP で認証成功
        """
        # OTP の生成
        otp_generator = pyotp.TOTP(self.user.secret_key)
        otp_token = otp_generator.now()

        response = self.client.post(self.verify_url, {"username": self.username, "otp": otp_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_otp_verification_invalid_otp(self):
        """
        ✅ 誤った OTP で認証失敗
        """
        response = self.client.post(self.verify_url, {"username": self.username, "otp": "123456"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid OTP.")

    def test_otp_verification_missing_fields(self):
        """
        ✅ OTP またはメールアドレスがない場合にエラー
        """
        response = self.client.post(self.verify_url, {"username": self.username})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.verify_url, {"otp": "123456"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
