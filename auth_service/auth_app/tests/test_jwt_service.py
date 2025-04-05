
import jwt
from django.test import TestCase

from auth_app.client.vault_client import VaultClient
from auth_app.services.jwt_service import generate_signed_jwt
from auth_app.settings import JWT_EXPIRATION


class JwtServiceTests(TestCase):
    def test_generate_signed_jwt_success(self):
        """
        VaultClientが正常に動作する場合、generate_signed_jwtが正しいJWTを生成することを確認。
        実際のVaultを使ってテストする
        """

        signed_jwt = generate_signed_jwt("12345", expires_in=JWT_EXPIRATION)

        self.assertIsNotNone(signed_jwt)
        self.assertTrue(isinstance(signed_jwt, str))
        self.assertIn(".", signed_jwt)

        payload = jwt.decode(signed_jwt, options={"verify_signature": False})
        self.assertEqual(payload["userId"], "12345")
