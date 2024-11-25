from django.shortcuts import HttpResponse, render
from rest_framework.decorators import api_view
from rest_framework.exceptions import JsonResponse, status
from .models import User, UserTwoFactorSetup, UserTwoFactorVerification
from django.core.mail import send_mail
from tfa.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.hashers import make_password
from .serializers import (
    UserSerializer,
    UserTwoFactorSetupSerializer,
    UserTwoFactorVerificationSerializer,
)

import pyotp
import datetime

SECRET_KEY = "secret_key"
OTP = "otp"


def generate_otp():
    secret_key = pyotp.random_base32()
    tocp = pyotp.TOTP(secret_key)
    otp = tocp.now()
    return {SECRET_KEY: secret_key, OTP: otp}


def send_otp_mail(to, otp):
    send_mail(
        "otp",
        "ワンタイムパスワードは以下です。\n"
        "5分以内にパスワードを入力してください。\n"
        f"パスワード：{otp}\n",
        DEFAULT_FROM_EMAIL,
        [to],
        fail_silently=False,
    )


@api_view(["POST"])
def otp_generate(request):
    serializer = UserTwoFactorSetupSerializer(data=request.data)
    if not serializer.is_valid():
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if User.objects.filter(username=username).exists():
        return HttpResponse(
            "User with this username already exists.", status=status.HTTP_409_CONFLICT
        )

    if UserTwoFactorSetup.objects.filter(username=username).exists():
        return HttpResponse(
            "User with this username already in signup phase.",
            status=status.HTTP_409_CONFLICT,
        )

    # パスワードとユーザーネーム両方が一致している時は、otp再発行

    otps = generate_otp()
    signup_user = UserTwoFactorSetup(
        username=username,
        email=email,
        otp_secret=otps[SECRET_KEY],
        password=make_password(password),
    )
    signup_user.save()
    send_otp_mail(email, otps[OTP])
    return HttpResponse("OTP sent successfully", status=status.HTTP_201_CREATED)


@api_view(["POST"])
def otp_verify(request):
    username = request.data.get("username")
    otp = request.data.get("otp")
    if not username or not otp:
        return JsonResponse(
            {"error": "Both 'username' and 'otp' fields are required."},
            status=400,
        )

    try:
        user_2fa = UserTwoFactorSetup.objects.get(username=username)
    except UserTwoFactorSetup.DoesNotExist:
        return JsonResponse(
            {"error": "User not found or not enrolled in 2FA."},
            status=404,
        )

    totp = pyotp.TOTP(user_2fa.otp_secret)
    if not totp.verify(otp):
        return JsonResponse({"error": "Invalid OTP."}, status=400)
    user_2fa.delete()
    return JsonResponse({"message": "OTP verified successfully."}, status=201)
