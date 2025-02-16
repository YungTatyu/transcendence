from auth_app.models import CustomUser
from auth_app.utils.redis_handler import RedisHandler
from rest_framework import serializers
from rest_framework.exceptions import APIException


class EmailConflictException(APIException):
    status_code = 409
    default_detail = "This email address is already in use."
    default_code = "email_conflict"


class UpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate_email(self, value):
        """メールアドレスの重複チェック"""
        user = self.context["user"]
        if (
            CustomUser.objects.filter(email=value)
            .exclude(user_id=user.user_id)
            .exists()
        ):
            raise EmailConflictException()
        redis_key = f"pending_email:{value}"
        if RedisHandler.exists(redis_key):
            raise EmailConflictException()
        return value

    def update(self, instance, validated_data):
        """ユーザーのメールアドレスを更新"""
        instance.email = validated_data["email"]
        instance.save()
        return instance
