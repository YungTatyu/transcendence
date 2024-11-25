from django.shortcuts import HttpResponse, render
from rest_framework.decorators import api_view
from rest_framework.exceptions import status
from .models import User, UserTwoFactorSetup, UserTwoFactorVerification
from django.core.mail import send_mail
from tfa.settings import DEFAULT_FROM_EMAIL
from .serializers import (
    UserSerializer,
    UserTwoFactorSetupSerializer,
    UserTwoFactorVerificationSerializer,
)

import pyotp

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
def signup(request):
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

    otps = generate_otp()
    signup_user = UserTwoFactorSetup(
        username=username,
        email=email,
        opt_secret=otps[SECRET_KEY],
    )
    signup_user.set_password(password)
    signup_user.save()
    send_otp_mail(email, otps[OTP])
    return HttpResponse("Signup successful.", status=status.HTTP_201_CREATED)
