from auth_app.models import CustomUser
from auth_app.services.otp_service import OTPService
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class OTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise AuthenticationFailed("Invalid password.")
        except CustomUser.DoesNotExist as err:
            raise serializers.ValidationError("Invalid email or password.") from err

        data["user"] = user
        return data


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField()

    def validate(self, data):
        email = data["email"]
        otp = data["otp"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist as err:
            raise serializers.ValidationError("Invalid email.") from err

        if not OTPService.verify_otp(user.secret_key, otp):
            raise serializers.ValidationError("Invalid OTP.")

        data["user"] = user
        return data
