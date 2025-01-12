from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import json

class OTPVerificationViewTestCase(APITestCase):
    def setUp(self):
        """テストデータの準備"""
        self.url = reverse('otp-verify')  # OTP検証エンドポイントのURL
        self.username = "testuser"
        self.valid_otp = "123456"
        self.invalid_otp = "000000"
        self.pending_user_data = {
            "username": self.username,
            "email": "testuser@example.com",
            "password_hash": "hashed_password123"
        }

    @patch('auth_app.utils.redis_handler.RedisHandler.get')  # RedisHandler.get メソッドのモック
    @patch('auth_app.utils.redis_handler.RedisHandler.delete')  # RedisHandler.delete メソッドのモック
    @patch('auth_app.views.OTPService.verify_otp')  # OTPService.verify_otp メソッドのモック
    def test_otp_verification_success(self, mock_verify_otp, mock_redis_get, mock_redis_delete):
        """OTP検証成功のテスト"""
        mock_verify_otp.return_value = True  # OTP検証に成功
        mock_redis_get.return_value = json.dumps(self.pending_user_data)  # 仮登録データがRedisに存在
        mock_redis_delete.return_value = None  # データ削除は成功したと仮定

        data = {"username": self.username, "otp": self.valid_otp}
        response = self.client.post(self.url, data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # アクセストークンとリフレッシュトークンがレスポンスに含まれることを確認
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # usernameクッキーが削除されることを確認
        self.assertNotIn("username", response.cookies)

        # RedisHandlerのgetとdeleteが呼び出されたか確認
        mock_redis_get.assert_called_once_with(key=f"pending_user:{self.username}")
        mock_redis_delete.assert_called_once_with(key=f"pending_user:{self.username}")

    @patch('auth_app.views.OTPService.verify_otp')  # OTPService.verify_otp メソッドのモック
    def test_otp_verification_invalid_otp(self, mock_verify_otp):
        """無効なOTPで検証する場合のテスト"""
        mock_verify_otp.return_value = False  # OTP検証失敗

        data = {"username": self.username, "otp": self.invalid_otp}
        response = self.client.post(self.url, data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # エラーメッセージが返されることを確認
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid OTP or username.")

    def test_otp_verification_missing_otp_fields(self):
        """必要なフィールドが欠けている場合のテスト"""
        data = {"username": self.username}  # OTPが欠けている
        response = self.client.post(self.url, data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # エラーメッセージが返されることを確認
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "username and otp are required.")

    @patch('auth_app.utils.redis_handler.RedisHandler.get')  # RedisHandler.get メソッドのモック
    @patch('auth_app.views.OTPService.verify_otp')  # OTPService.verify_otp メソッドのモック
    def test_otp_verification_no_pending_user_data(self, mock_verify_otp, mock_redis_get):
        """Redisに仮登録データが存在しない場合のテスト"""
        mock_verify_otp.return_value = True  # OTP検証に成功
        mock_redis_get.return_value = None  # Redisにデータが存在しない

        data = {"username": self.username, "otp": self.valid_otp}
        response = self.client.post(self.url, data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # エラーメッセージが返されることを確認
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "No pending user data found.")
