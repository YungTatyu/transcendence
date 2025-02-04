from rest_framework import serializers

from .models import User

class createUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)

class searchUserSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    username = serializers.CharField(max_length=10)
    avatarPath = serializers.CharField(max_length=100)
