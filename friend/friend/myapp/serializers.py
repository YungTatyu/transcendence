from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'password']

		def create(self, validated_data):
			user = User.objects.create_user(
				username=validated_data['username'],
				password=validated_data['password']
			)
			return user
		
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = FriendRequest
		fields = ['from_user', 'to_user', 'status']