import json
import logging
from typing import Optional

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.client.jwt_utils import (
    add_signature_to_jwt,
    create_unsigned_jwt,
)
from auth_app.client.user_client import UserClient
from auth_app.client.vault_client import VaultClient
from auth_app.models import CustomUser
from auth_app.serializers.signup_serializer import (
    OTPVerificationSerializer,
    SignupSerializer,
)
from auth_app.services.otp_service import OTPService
from auth_app.settings import CA_CERT, CLIENT_CERT, CLIENT_KEY, VAULT_ADDR, COOKIE_DOMAIN

from auth_app.utils.redis_handler import RedisHandler

logger = logging.getLogger(__name__)


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        # リクエストデータをシリアライザで検証
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warn("invalid request body")
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        # 仮登録データ取得
        user_data = serializer.save()

        qr_code_base64 = OTPService.generate_qr_code(
            email=user_data["email"], secret=user_data["otp_secret"]
        )

        # Cookieにemailを設定しレスポンスを返す
        response = Response({"qr_code": qr_code_base64}, status=status.HTTP_200_OK)
        response.set_cookie(
            key="email",
            value=user_data["email"],
            httponly=True,
            secure=True,
            path="/",
            max_age=300,
        )
        return response


class OTPVerificationView(APIView):
    """
    サインアップ時のOTP検証
    """

    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data["username"]
        otp_token = serializer.validated_data["otp"]

        # Redisから仮登録データを取得
        user_data = self.__get_pending_user_data(username)
        if not user_data:
            logger.warn("No pending user data found.")
            return Response(
                {"error": "No pending user data found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        secret = user_data.get("otp_secret")
        if not secret:
            logger.debug("there no secret")
            return Response(
                {"error": "Failed to fetch user secret"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if not OTPService.verify_otp(secret, otp_token):
            logger.warn("Invalid OTP or secret.")
            return Response(
                {"error": "Invalid OTP or secret."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = self.__register_user(user_data)
        if user_id is None:
            logger.fatal("Failed to register user.")
            return Response(
                {"error": "Failed to register user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        self.__cleanup_pending_user(username)

        client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)

        # TODO userIDを取得する

        token = client.fetch_token()
        if not token:
            logger.error("Failed to fetch token from Vault")
            return Response(
                {"error": "Token fetch failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        jwt_header = {"alg": "RS256", "typ": "JWT"}
        jwt_payload = {"sub": "1234567890", "userId": "1"}
        jwt_data = create_unsigned_jwt(jwt_header, jwt_payload)
        signature = client.fetch_signature(token, jwt_data)
        signed_jwt = add_signature_to_jwt(jwt_data, signature)

        # extracted_signature = extract_signature_from_jwt(signed_jwt)
        # pubkey = client.fetch_pubkey(token)
        # if extracted_signature and pubkey:
        #     logger.error("Verify JWT: ", verify_jwt(pubkey, jwt_data, extracted_signature))

        # TODO 署名を組み込んだJWTの生成
        tokens = {
             "access": signed_jwt,
            # refresh tokenの生成方法も要検討
            "refresh": jwt.encode({"user_id": user_id}, None, algorithm=None),

        }

        response = Response(
            {
                "message": "OTP verification successful.",
                "userId": user_id,
                "accessToken": tokens.get("access"),
            },
            status=status.HTTP_200_OK,
        )

        # JWT を HttpOnly Cookie に保存
        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,  # JavaScript からアクセス不可 (XSS 対策)
            secure=True,
            samesite="None",
            path="/",
            domain=COOKIE_DOMAIN,  # 親ドメインを設定
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            domain=COOKIE_DOMAIN,  # 親ドメインを設定
        )

        # emailクッキーを削除
        response.delete_cookie("email", path="/")
        return response

    def __get_pending_user_data(self, username: str) -> dict:
        """
        Redisから仮登録データを取得する
        :param username: ユーザー名
        :return: 仮登録データまたはNone
        """
        redis_key = f"pending_user:{username}"
        redis_data = RedisHandler.get(key=redis_key)

        if not redis_data:
            return None

        return json.loads(redis_data)

    def __register_user(self, user_data: dict) -> Optional[int]:
        """
        本登録データをデータベースに保存する
        :param user_data: 仮登録データ
        :return: 保存成功ならTrue、失敗ならFalse
        """
        client = UserClient(
            base_url=settings.USER_API_BASE_URL, use_mock=settings.USER_API_USE_MOCK
        )
        try:
            res = client.create_user(user_data["username"])
            user_id = res.json()["userId"]

            CustomUser.objects.create_user(
                user_id=user_id,
                email=user_data["email"],
                secret_key=user_data["otp_secret"],
                hashed_password=user_data["password_hash"],
            )

            return user_id
        except Exception as e:
            logger.error(f"Error saving user: {str(e)}")
            return None

    def __cleanup_pending_user(self, username: str) -> None:
        """
        Redisから仮登録データを削除する
        :param username: ユーザー名
        """
        redis_key = f"pending_user:{username}"
        RedisHandler.delete(key=redis_key)
