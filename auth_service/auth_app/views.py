import jwt
import datetime
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer 
from auth_app.services.otp_service import OTPService
import logging
logger = logging.getLogger(__name__)

# TODO csrf_exempt
@csrf_exempt
def generate_jwt(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"detail": "Invalid credentials"}, status=403)

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }

    try:
        with open(settings.JWT_PRIVATE_KEY_PATH, 'r') as f:
            private_key = f.read()

        token = jwt.encode(payload, private_key, algorithm='RS256')

        return JsonResponse({"access_token": token})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_public_key(request):
    try:
        with open(settings.JWT_PUBLIC_KEY_PATH, 'r') as f:
            public_key = f.read()
        return JsonResponse({"public_key": public_key})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        # リクエストデータをシリアライザで検証
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 仮登録データ取得
        user_data = serializer.save()
        username = user_data["username"]

        qr_code_base64 = OTPService.generate_qr_code(email=user_data["email"], secret=user_data["otp_secret"])

        # Cookieにユーザー名を設定しレスポンスを返す
        response = Response(
            {"qr_code": qr_code_base64}, 
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="username",
            value=username,
            httponly=True,
            secure=True,
            path="/",
            max_age=300
        )
        return response

class OTPVerificationView(APIView):
    """
    サインアップ時のOTP検証
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        otp_token = request.data.get("otp")

        if not username or not otp_token:
            return Response({"error": "username and otp are required."}, status=status.HTTP_400_BAD_REQUEST)

        # OTPの検証
        if OTPService.verify_otp(username, otp_token):
            # クッキーを削除
            response = Response(
                {
                    "access": "tmp",
                    "refresh": "refresh_token_placeholder",  # refresh tokenの生成方法も要検討
                },
                status=status.HTTP_200_OK,
            )

            # usernameクッキーを削除
            response.delete_cookie("username", path="/")
            return response
        else:
            return Response(
                {"error": "Invalid OTP or username."},
                status=status.HTTP_400_BAD_REQUEST,
            )