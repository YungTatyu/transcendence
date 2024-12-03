from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["POST"])
def logout(request):
    jwt_auth = JWTAuthentication()
    user, token = jwt_auth.authenticate(request)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    refresh_token = request.data.get("refresh")
    if refresh_token is None:
        return Response(
            {"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token_obj = RefreshToken(refresh_token)
        token_obj.blacklist()
    except Exception as e:
        return Response(
            {"error": "Failed to blacklist token", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
