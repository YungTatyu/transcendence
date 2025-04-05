
import jwt
from django.test import TestCase

from auth_app.services.jwt_service import generate_signed_jwt, verify_signed_jwt, extract_signature_from_jwt, verify_jwt
from auth_app.settings import JWT_EXPIRATION
from auth_app.client.vault_client import VaultClient
from auth_app.settings import (
    CA_CERT,
    CLIENT_CERT,
    CLIENT_KEY,
    JWT_EXPIRATION,
    VAULT_ADDR,
)

class JwtServiceTests(TestCase):
    def test_generate_signed_jwt_success(self):
        """
        generate_signed_jwtが正しいJWTを生成する。
        """

        signed_jwt = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)

        self.assertIsNotNone(signed_jwt)
        self.assertTrue(isinstance(signed_jwt, str))
        self.assertIn(".", signed_jwt)

        payload = jwt.decode(signed_jwt, options={"verify_signature": False})
        self.assertEqual(payload["userId"], "12345")

    def test_verify_signed_jwt_success(self):
        """
        verify_signed_jwtが正しく署名を検証する。
        """

        # JWTを生成して検証
        signed_jwt = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)
        result = verify_signed_jwt(signed_jwt)

        # JWTが正しく検証されることを確認
        self.assertTrue(result)

    def test_verify_jwt_success(self):
        """
        verify_jwt が正しく署名を検証する
        """
        # 正常な JWT を生成
        user_id = "12345"
        signed_jwt = generate_signed_jwt(user_id)
        self.assertIn(".", signed_jwt)

        client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)

        token = client.fetch_token()
        pubkey = client.fetch_pubkey(token)
        self.assertIsNotNone(pubkey, "公開鍵の取得に失敗")

        extracted_signature = extract_signature_from_jwt(signed_jwt)
        result = verify_jwt(pubkey, signed_jwt.encode(), extracted_signature)

        self.assertTrue(result, "JWT の署名検証に失敗しました")

