from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.utils.redis_handler import RedisHandler
import json

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
        redis_key = validated_data["username"]
        
        # 仮登録情報をRedisに保存
        redis_data = {
            "username": validated_data["username"],
            "email": validated_data["email"],
            "password": validated_data["password"],
        }

        # Redisに仮登録情報を保存
        RedisHandler.set(redis_key, json.dumps(redis_data), timeout=3600)  # 1時間の有効期限

        # 仮登録用のデータを返す
        return validated_data  # ユーザー情報をそのまま返す