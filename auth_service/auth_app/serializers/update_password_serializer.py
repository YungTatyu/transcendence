from rest_framework import serializers
from django.core.exceptions import ValidationError
from auth_app.models import CustomUser
from django.contrib.auth.hashers import check_password, make_password

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate_new_password(self, value):
        user = self.context["user"]

        if not user.check_password(self.current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})
        return value
