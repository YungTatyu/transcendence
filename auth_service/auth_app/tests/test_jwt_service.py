from django.test import TestCase
from unittest.mock import patch
from auth_app.services.jwt_service import generate_signed_jwt, verify_signed_jwt
from auth_app.settings import JWT_EXPIRATION


class JwtServiceTests(TestCase):

    @patch("auth_app.services.jwt_service.client")
    def test_generate_signed_jwt_success(self, mock_client):
        """
        VaultClient のメソッドが正常に動作する場合、generate_signed_jwt が正しい JWT を生成することを確認
        """
        mock_client.fetch_token.return_value = "mock-token"
        mock_client.fetch_signature.return_value = "mock-signature"

        result = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)

        self.assertIsNotNone(result)
        self.assertEqual(result.count('.'), 2)

    @patch("auth_app.services.jwt_service.client")
    def test_generate_signed_jwt_failure_no_token(self, mock_client):
        """
        VaultClient がトークンを返さない場合、generate_signed_jwt が None を返すことを確認
        """
        mock_client.fetch_token.return_value = None
        result = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)
        self.assertIsNone(result)

    @patch("auth_app.services.jwt_service.client")
    def test_generate_signed_jwt_failure_no_signature(self, mock_client):
        """
        VaultClient が署名を返さない場合、generate_signed_jwt が None を返すことを確認
        """
        mock_client.fetch_token.return_value = "mock-token"
        mock_client.fetch_signature.return_value = None
        result = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)
        self.assertIsNone(result)

    @patch("auth_app.services.jwt_service.client")
    def test_verify_signed_jwt_success(self, mock_client):
        """
        verify_signed_jwt が有効な JWT に対して True を返すことを確認
        """
        mock_client.fetch_token.return_value = "mock-token"
        mock_client.fetch_pubkey.return_value = "mock-pubkey"

        with patch("auth_app.services.jwt_service.extract_signature_from_jwt", return_value="mock-signature"):
            with patch("auth_app.services.jwt_service.verify_jwt", return_value=True):
                token = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)
                self.assertTrue(verify_signed_jwt(token))

    @patch("auth_app.services.jwt_service.client")
    def test_verify_signed_jwt_failure_no_token(self, mock_client):
        """
        VaultClient がトークンを返さない場合、verify_signed_jwt が False を返すことを確認
        """
        mock_client.fetch_token.return_value = None
        token = "invalid-token"
        self.assertFalse(verify_signed_jwt(token))

    @patch("auth_app.services.jwt_service.client")
    def test_verify_signed_jwt_failure_no_pubkey(self, mock_client):
        """
        VaultClient が公開鍵を返さない場合、verify_signed_jwt が False を返すことを確認
        """
        mock_client.fetch_token.return_value = "mock-token"
        mock_client.fetch_pubkey.return_value = None
        token = "invalid-token"
        self.assertFalse(verify_signed_jwt(token))

    @patch("auth_app.services.jwt_service.client")
    def test_verify_signed_jwt_failure_invalid_signature(self, mock_client):
        """
        署名が無効な場合、verify_signed_jwt が False を返すことを確認
        """
        mock_client.fetch_token.return_value = "mock-token"
        mock_client.fetch_pubkey.return_value = "mock-pubkey"

        with patch("auth_app.services.jwt_service.extract_signature_from_jwt", return_value="invalid-signature"):
            self.assertFalse(verify_signed_jwt("invalid-token"))

    @patch("auth_app.services.jwt_service.client")
    def test_verify_signed_jwt_failure_expired(self, mock_client):
        """
        JWT が期限切れの場合、verify_signed_jwt が False を返すことを確認
        """
        mock_client.fetch_token.return_value = "mock-token"
        mock_client.fetch_pubkey.return_value = "mock-pubkey"

        expired_jwt = "expired-token"  # 有効期限が過ぎたトークンと仮定
        self.assertFalse(verify_signed_jwt(expired_jwt))
