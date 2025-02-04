from rest_framework import serializers

from .models import User

class createUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)

