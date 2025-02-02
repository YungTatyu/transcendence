import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.client.user_client import UserClient
from auth_app.models import CustomUser
from auth_app.services.otp_service import OTPService

logger = logging.getLogger(__name__)


class OTPLoginView(APIView):
    """
    既存ユーザーのログイン処理
    """

    def post(self, request, *args, **kwargs):
        """
        1. ユーザー名とパスワードで認証
        2. 認証成功後、OTP 検証ステップへ進む
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            logger.warn("Invalid request: missing username or password")
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 認証を試みる
        client = UserClient(
            base_url=settings.USER_API_BASE_URL,
            use_mock=settings.USER_API_USE_MOCK,
            mock_search_data={"userId": "12345", "username": "mockuser"},
        )
        try:
            # `username` でユーザーを検索
            res = client.search_users({"username": username})
            user_data = res.json()
            if not user_data or "userId" not in user_data:
                raise ValueError("User not found")
            user_id = user_data["userId"]

            user = CustomUser.objects.get(user_id=user_id)
            if not user.check_password(password):  # パスワードをチェック
                raise ValueError("Invalid password")

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # OTP 認証の開始メッセージを返す
        response = Response(
            {
                "message": "Use the OTP generated by your authentication app to complete the login process."
            },
            status=status.HTTP_200_OK,
        )

        # `username` を Cookie に保存
        response.set_cookie(
            key="username",
            value=username,
            httponly=True,
            secure=True,
            path="/",
            max_age=300,
        )

        logger.info(f"OTP login initiated for user: {username}")
        return response


class OTPLoginVerificationView(APIView):
    """
    OTP の検証
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        otp_token = request.data.get("otp")

        if not username or not otp_token:
            logger.warn("Invalid request body: missing username or otp")
            return Response(
                {"error": "Username and OTP are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not OTPService.verify_otp(username, otp_token):
            logger.warn(f"Invalid OTP for user: {username}")
            return Response(
                {"error": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # トークン発行 (本来は JWT トークンを発行する)
        response = Response(
            {
                "access": "generated_access_token",
                "refresh": "generated_refresh_token",
            },
            status=status.HTTP_200_OK,
        )

        # `username` Cookie を削除
        response.delete_cookie("username", path="/")

        logger.info(f"OTP verified successfully for user: {username}")
        return response
