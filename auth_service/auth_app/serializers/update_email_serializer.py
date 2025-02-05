from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from auth_app.models import CustomUser
from auth_app.utils.redis_handler import RedisHandler

class UpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """メールアドレスの重複チェック"""
        user = self.context["user"]
        if CustomUser.objects.filter(email=value).exclude(user_id=user.user_id).exists():
            raise serializers.ValidationError("This email address is already in use.")
        redis_key = f"pending_email:{value}"
        if RedisHandler.exists(redis_key):
            raise serializers.ValidationError(
                "This email is already pending registration."
            )
        return value

    def update(self, instance, validated_data):
        """ユーザーのメールアドレスを更新"""
        instance.email = validated_data["email"]
        instance.save()
        return instance
