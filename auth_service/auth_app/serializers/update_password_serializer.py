from rest_framework import serializers
from django.core.exceptions import ValidationError
from auth_app.models import CustomUser
from django.contrib.auth.hashers import check_password, make_password

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate(self, data):
        """現在のパスワードをチェック & 新しいパスワードと比較"""
        user = self.context["user"]
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        # 現在のパスワードが正しいか検証
        if not user.check_password(current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        # 新しいパスワードが現在のパスワードと同じでないかチェック
        if current_password == new_password:
            raise serializers.ValidationError({"new_password": "New password must be different from the current password."})

        return data
