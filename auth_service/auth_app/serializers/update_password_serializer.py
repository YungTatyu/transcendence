from rest_framework import serializers
from django.core.exceptions import ValidationError
from auth_app.models import CustomUser
from django.contrib.auth.hashers import check_password, make_password

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate_password(self, value):
        """メールアドレスの重複チェック"""
        user = self.context["user"]

        if not check_password(self.current_password, user.password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})
        return value
