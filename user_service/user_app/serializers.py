from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)


class SearchUserSerializer(serializers.Serializer):
    userId = serializers.IntegerField(source="user_id")
    username = serializers.CharField(max_length=10)
    avatarPath = serializers.CharField(max_length=100, source="avatar_path")
