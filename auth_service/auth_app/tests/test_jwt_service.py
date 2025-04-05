
import jwt
from django.test import TestCase

from auth_app.services.jwt_service import generate_signed_jwt, verify_signed_jwt
from auth_app.settings import JWT_EXPIRATION


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
