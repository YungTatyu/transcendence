from django.shortcuts import render

from rest_framework.authtoken.models import Token
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .serializers import UserSerializer

class RegisterUser(APIView):
	def post(self, request):
		serializer = UserSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"messsage": "User created successfly!"}, status = status.HTTP_201_CREATED)
		return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import authenticate

class LoginUser(APIView):
	def post(self, request):
		username = request.data.gte('username')
		password = request.data.get('password')
		user = authenticate(username = username, password = password)
		if user is not None:
			token, _= Token.objects.get_or_create(user=user)
			return  Response({"token": "token.key"}, status=status.HTTP_200_OK)
		return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
	
from .serializers import FriendRequestSerializer
from .models import FriendRequest
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import serializers

class FriendRequestView(APIView):
	serializer_class = FriendRequestSerializer
	permission_classes = [IsAuthenticated]
	def post(self, request):
		serializer = FriendRequestSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"message": "Friend request sent!"}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		from_user = self.request.user  # 現在ログイン中のユーザー
		User = get_user_model()
		to_user = User.objects.get(username=self.request.data.get('to_user'))
		if from_user == to_user:
			raise serializers.ValidationError("You cannot send a friend request to yourself.")
		serializer.save(from_user=from_user, to_user=to_user)
	
class FriendRequestActionView(APIView):
	def post(self, request, pk):
		try:
			friend_request = FriendRequest.objects.get(pk=pk)
		except FriendRequest.DoesNotExist:
			return Response({"error": "Friend request not found"}, status= status.HTTP_404_NOT_FOUND)
		
		action = request.data.get('action')
		if action == 'accept':
			friend_request.status = 'accepted'
			friend_request.save()
			return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
		elif action == 'reject':
			friend_request.status = 'rejected'
			friend_request.save()
			return Response({"message": "Friend request rejected"}, status+status.HTTP_200_OK)
		return Response ({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)