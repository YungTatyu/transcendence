import json

import pyotp
from auth_app.client.user_client import UserClient
from auth_app.models import CustomUser
from auth_app.utils.redis_handler import RedisHandler
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        # Redisで仮登録状態を確認
        redis_key = f"pending_email:{value}"
        if RedisHandler.exists(redis_key):
            raise serializers.ValidationError(
                "This email is already pending registration."
            )
        return value

    def validate_username(self, value):
        client = UserClient(
            base_url=settings.USER_API_BASE_URL, use_mock=settings.USER_API_USE_MOCK
        )
        res = client.search_users({"username": value})
        if res.status_code == 200:
            raise serializers.ValidationError("This username is already in use.")

        # Redisで仮登録状態を確認
        redis_key = f"pending_user:{value}"
        if RedisHandler.exists(redis_key):
            raise serializers.ValidationError(
                "This username is already pending registration."
            )
        return value

    def create(self, validated_data):
        """
        仮登録をRedisに保存する
        ユーザー名をキーとして使用し、ユーザー情報をRedisに保存
        """
        # Redisキーとしてユーザー名とemailを使用
        redis_key_user = f"pending_user:{validated_data['username']}"
        redis_key_email = f"pending_email:{validated_data['email']}"

        # パスワードをハッシュ化
        hashed_password = make_password(validated_data["password"])

        # OTP秘密鍵を生成
        otp_secret = pyotp.random_base32()

        # 仮登録情報をRedisに保存
        redis_data = {
            "username": validated_data["username"],
            "email": validated_data["email"],
            "password_hash": hashed_password,
            "otp_secret": otp_secret,  # OTPの秘密鍵
        }

        RedisHandler.set(
            redis_key_user, json.dumps(redis_data), timeout=3600
        )  # 1時間の有効期限

        # 重複チェックのためRedisキーとしてEmailを使用
        RedisHandler.set(
            redis_key_email, validated_data["username"], timeout=3600
        )  # 1時間の有効期限

        # 仮登録用のデータを返す
        return {
            "username": validated_data["username"],
            "email": validated_data["email"],
            "otp_secret": otp_secret,
        }
