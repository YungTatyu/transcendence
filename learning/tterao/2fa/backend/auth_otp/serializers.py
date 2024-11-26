from rest_framework import serializers
from .models import User, UserTwoFactorSetup, UserTwoFactorVerification


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["__all__"]


class UserTwoFactorSetupSerializer(serializers.Serializer):
    class Meta:
        model = UserTwoFactorSetup
        fields = ["__all__"]


class UserTwoFactorVerificationSerializer(serializers.Serializer):
    class Meta:
        model = UserTwoFactorVerification
        fields = ["__all__"]
