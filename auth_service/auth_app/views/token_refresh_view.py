import logging

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from auth_app.services import jwt_service

logger = logging.getLogger(__name__)


class TokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return JsonResponse(
                {"error": "Refresh token is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_valid = jwt_service.verify_signed_jwt(refresh_token)
        if not is_valid:
            return JsonResponse(
                {"error": "Refresh token is missing or invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            payload = jwt_service.jwt.decode(
                refresh_token,
                options={"verify_signature": False}
            )
            user_id = payload.get("userId")
            if not user_id:
                return JsonResponse(
                    {"error": "Invalid refresh token payload."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            new_access_token = jwt_service.generate_signed_jwt(user_id)
            if not new_access_token:
                return JsonResponse(
                    {"error": "Failed to generate new access token."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response = JsonResponse({"accessToken": new_access_token})
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                path="/",
            )
            return response

        except Exception as e:
            logger.exception("Unexpected error during token refresh")
            return JsonResponse(
                {"error": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
