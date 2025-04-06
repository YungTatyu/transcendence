import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.services import jwt_service
from auth_app.settings import (
    COOKIE_DOMAIN,
)

logger = logging.getLogger(__name__)


class TokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            is_valid = jwt_service.verify_signed_jwt(refresh_token)
        except Exception:
            logger.exception("Error verifying signed JWT")
            return Response(
                {"error": "Refresh token is missing or invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not is_valid:
            return Response(
                {"error": "Refresh token is missing or invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            payload = jwt_service.jwt.decode(
                refresh_token, options={"verify_signature": False}
            )
            user_id = payload.get("user_id")
            if not user_id:
                return Response(
                    {"error": "Invalid refresh token payload."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            new_access_token = jwt_service.generate_signed_jwt(user_id)
            if not new_access_token:
                return Response(
                    {"error": "Failed to generate new access token."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response = Response({"accessToken": new_access_token})
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None",
                domain=COOKIE_DOMAIN,
                path="/",
            )
            return response

        except Exception:
            logger.exception("Unexpected error during token refresh")
            return Response(
                {"error": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
