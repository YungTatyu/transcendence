from rest_framework.decorators import api_view
from rest_framework.exceptions import JsonResponse, bad_request, status
from .models import User, UserTwoFactorSetup, UserTwoFactorVerification
from django.core.mail import send_mail
from tfa.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    UserSerializer,
    UserTwoFactorSetupSerializer,
    UserTwoFactorVerificationSerializer,
)

import pyotp

SECRET_KEY = "secret_key"
OTP = "otp"
INTERVAL_TIME = 60


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def generate_totp(secret_key):
    return pyotp.TOTP(secret_key, interval=INTERVAL_TIME)


def generate_otp(secret_key=pyotp.random_base32()):
    totp = generate_totp(secret_key)
    otp = totp.now()
    return {SECRET_KEY: secret_key, OTP: otp}


def send_otp_mail(to, otp):
    send_mail(
        "otp",
        "ワンタイムパスワードは以下です。\n"
        "1分以内にパスワードを入力してください。\n"
        f"パスワード：{otp}\n",
        DEFAULT_FROM_EMAIL,
        [to],
        fail_silently=False,
    )


@api_view(["POST"])
def otp_generate(request):
    serializer = UserTwoFactorSetupSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "Both 'username' and 'otp' fields are required."},
            status=status.HTTP_409_CONFLICT,
        )

    if UserTwoFactorSetup.objects.filter(username=username).exists():
        return JsonResponse(
            {"error:" "User with this username already in signup phase."},
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
    response = JsonResponse(
        {"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED
    )
    response.set_cookie("username", username)
    return response


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

    totp = generate_totp(user_2fa.otp_secret)
    if not totp.verify(otp):
        return JsonResponse({"error": "Invalid OTP."}, status=400)

    email = user_2fa.email
    password = user_2fa.password
    user = User(
        username=username,
        password=password,
        email=email,
    )
    user.save()

    tokens = generate_tokens_for_user(user)
    user_2fa.delete()
    response = JsonResponse(tokens, status=201)
    response.delete_cookie("username")
    return response


# resend top
# if top is expired, regenerate top
@api_view(["POST"])
def otp_resend(request):
    username = request.data.get("username")
    if not username:
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

    #  otpを再発行
    otps = generate_otp()
    user_2fa.otp_secret = otps[SECRET_KEY]
    user_2fa.save()

    send_otp_mail(user_2fa.email, otps[OTP])
    return JsonResponse({"message": "OTP regenerated."}, status=201)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return JsonResponse(
            {"error": "Both 'username' and 'password' fields are required."},
            status=400,
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse(
            {"error": "invalid username or password."}, status=status.HTTP_404_NOT_FOUND
        )

    if UserTwoFactorVerification.objects.filter(user=user).exists():
        return JsonResponse(
            {"error": "User with this username already in otp phase."},
            status=status.HTTP_409_CONFLICT,
        )

    otps = generate_otp()
    tfa_user = UserTwoFactorVerification(
        user=user,
        otp_secret=otps[SECRET_KEY],
    )
    tfa_user.save()

    send_otp_mail(user.email, otps[OTP])
    response = JsonResponse(
        {"message": "OTP generated."}, status=status.HTTP_201_CREATED
    )
    request.session["username"] = username
    response.set_cookie("username", username)
    return response


@api_view(["POST"])
def login_otp_verify(request):
    username = request.data.get("username")
    otp = request.data.get("otp")
    if not username or not otp:
        return JsonResponse(
            {"error": "Both 'username' and 'otp' fields are required."},
            status=400,
        )

    try:
        user = User.objects.get(username=username)
        tfa_user = UserTwoFactorVerification.objects.get(user=user)
    except UserTwoFactorVerification.DoesNotExist:
        return JsonResponse(
            {"error": "User not found or not enrolled in 2FA."},
            status=404,
        )

    totp = generate_totp(tfa_user.otp_secret)
    if not totp.verify(otp):
        return JsonResponse({"error": "Invalid OTP."}, status=400)

    tfa_user.delete()
    tokens = generate_tokens_for_user(user)
    response = JsonResponse(tokens, status=200)
    response.delete_cookie("username")
    return response


@api_view(["POST"])
def login_otp_resend(request):
    username = request.data.get("username")
    if not username:
        return JsonResponse(
            {"error": "'username' fields are required."},
            status=400,
        )
    try:
        user = User.objects.get(username=username)
        user_2fa = UserTwoFactorVerification.objects.get(user=user)
    except UserTwoFactorVerification.DoesNotExist:
        return JsonResponse(
            {"error": "User not found or not enrolled in 2FA."},
            status=404,
        )

    #  otpを再発行
    otps = generate_otp()
    user_2fa.otp_secret = otps[SECRET_KEY]
    user_2fa.save()

    send_otp_mail(user.email, otps[OTP])
    return JsonResponse({"message": "OTP regenerated."}, status=201)


@api_view(["POST"])
def logout(request):
    user, token = JWTAuthentication.authenticate(request)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    token = RefreshToken(token)
    token.blacklist()
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
