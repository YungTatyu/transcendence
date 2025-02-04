from rest_framework import serializers
from auth_app.models import CustomUser
from auth_app.services.otp_service import OTPService


class OTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid email or password.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        data["user"] = user
        return data


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data["email"]
        otp_token = data["otp"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email.")

        if not OTPService.verify_otp(user.secret_key, otp_token):
            raise serializers.ValidationError("Invalid OTP.")

        data["user"] = user
        return data
