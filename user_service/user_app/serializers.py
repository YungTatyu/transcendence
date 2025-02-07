from rest_framework import serializers

from .models import User

class createUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)

class searchUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=10)
    avatar_path = serializers.CharField(max_length=100)
