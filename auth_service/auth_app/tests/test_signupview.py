from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

class SignupViewTestCase(APITestCase):
    def setUp(self):
        """テストデータの準備"""
        self.url = reverse('otp-signup')  # URLパターン名に基づいてURLを取得
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
        self.invalid_data = {
            "username": "",
            "email": "invalid-email",
            "password": "short"
        }

    @patch('auth_app.utils.redis_handler.RedisHandler.set')  # RedisHandler.set メソッドのモック
    def test_signup_success(self, mock_redis_set):
        """正常なサインアップのテスト"""

        # mock_redis_setを呼び出しができるようにしておく
        mock_redis_set.return_value = True

        response = self.client.post(self.url, self.valid_data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # QRコードがレスポンスに含まれていることを確認
        self.assertIn('qr_code', response.data)

        # Cookieの設定確認
        self.assertIn('username', response.cookies)
        self.assertEqual(response.cookies['username'].value, self.valid_data['username'])

        # Redisに仮登録情報が保存されたか確認
        mock_redis_set.assert_called_once()

    def test_signup_invalid_data(self):
        """無効なデータでサインアップする場合のテスト"""

        response = self.client.post(self.url, self.invalid_data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # エラーメッセージが返されることを確認
        self.assertIn("error", response.data)

    def test_signup_missing_field(self):
        """必要なフィールドが欠けている場合のテスト"""

        invalid_data = {
            "username": "testuser", 
            "email": "testuser@example.com"
            # password フィールドが欠けている
        }

        response = self.client.post(self.url, invalid_data, format='json')

        # ステータスコードの確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # エラーメッセージが返されることを確認
        self.assertIn("error", response.data)
