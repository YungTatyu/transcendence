from unittest.mock import patch
from django.test import TestCase
from auth_app.services.otp_service import OTPService
import pyotp
import json

class OTPServiceTestCase(TestCase):
    @patch("auth_app.utils.redis_handler.RedisHandler.set")
    def test_generate_qr_code(self, mock_redis_set):
        # username = "testuser"
        email = "testuser@example.com"
        otp_secret = pyotp.random_base32()

        # QRコード生成
        qr_code_base64 = OTPService.generate_qr_code(email=email, secret=otp_secret)

        # # QRコードが生成されていることを確認
        self.assertTrue(qr_code_base64.startswith("data:image/png;base64,"))

    @patch("auth_app.utils.redis_handler.RedisHandler.get")
    def test_verify_otp(self, mock_redis_get):
        username = "testuser"
        secret = pyotp.random_base32()
        otp = pyotp.TOTP(secret)

        # 仮登録情報をRedisに模倣したデータとして設定
        redis_data = json.dumps({
            "username": username,
            "email": "testuser@example.com",
            "otp_secret": secret
        })

        # Redisから秘密鍵を含む仮登録データを取得するモックを設定
        mock_redis_get.return_value = redis_data

        # 正しいOTPトークンを検証
        valid_token = otp.now()
        self.assertTrue(OTPService.verify_otp(username=username, otp_token=valid_token))

        # 無効なOTPトークンを検証
        invalid_token = "000000"
        self.assertFalse(OTPService.verify_otp(username=username, otp_token=invalid_token))
