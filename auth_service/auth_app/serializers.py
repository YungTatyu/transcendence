from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.utils.redis_handler import RedisHandler
import json
from django.contrib.auth.hashers import make_password
import pyotp
class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        """
        仮登録をRedisに保存する
        ユーザー名をキーとして使用し、ユーザー情報をRedisに保存
        """
        # Redisキーとしてユーザー名を使用
        redis_key = f"pending_user:{validated_data['username']}"

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
        RedisHandler.set(redis_key, json.dumps(redis_data), timeout=3600)  # 1時間の有効期限

        # 仮登録用のデータを返す
        return {
            "username": validated_data["username"],
            "email": validated_data["email"],
            "otp_secret": otp_secret,
        }
