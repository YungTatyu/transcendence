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
from io import BytesIO
import base64
import pyotp
import qrcode
from .serializers import SignupSerializer 

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
        user_data = serializer.validated_data
        username = user_data["username"]

        # OTP用シークレット生成とQRコードデータ作成
        secret = pyotp.random_base32()
        otp = pyotp.TOTP(secret)
        qr_code_data = otp.provisioning_uri(
            name=user_data["email"], 
            issuer_name="YourApp"
        )

        # QRコードを生成しBase64エンコード
        qr_code_base64 = self._generate_base64_qr_code(qr_code_data)

        # Cookieにユーザー名を設定しレスポンスを返す
        response = JsonResponse(
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

    def _generate_base64_qr_code(self, data: str) -> str:
        """QRコードを生成してBase64エンコードする"""
        img = qrcode.make(data)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        return qr_code_base64