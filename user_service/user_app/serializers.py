from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)


class SearchUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=10)
    avatar_path = serializers.CharField(max_length=100)
