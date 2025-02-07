from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,\
	 							 HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .serializers import UserIdValidator,FriendsSerializer
from .models import Friends
from django.db.models import Q
#修正の必要あり. DBの変更

from datetime import datetime
from django.utils.timezone import now 

class FriendListView(APIView):
	'''
	usernameはどこから？
	'''
	def get(self, request):
		from_user_id = 1
		user_name = "kazuki"
		# friends = Friends.objects.filter((Q(from_user_id=from_user_id) | Q(to_user_id=from_user_id)) & Q(status="approved"))
		friends = Friends.objects.filter(Q(from_user_id=from_user_id) | Q(to_user_id=from_user_id))
		if not friends:
			return Response({"error": "Friend not found."}, status=HTTP_404_NOT_FOUND)
		serializer = FriendsSerializer(friends, many=True)
		friends_data = []
		for friend in serializer.data:
			if friend['from_user_id'] == 1:
				tmp = {
                    "userId": friend['to_user_id'],  # 'from_user_id' を使ってアクセス
                    "username": "test",  # 仮のユーザー名（例えば 'test'）
                    "status": friend['status'],
                    "request_sent_at": friend['request_sent_at'],
                    "approved_at": friend['approved_at']
                }
			else:
				'''
				pendingの時、表示する必要はあるか
				'''
				tmp = {
                    "userId": friend['from_user_id'],  # 'from_user_id' を使ってアクセス
                    "username": "test",  # 仮のユーザー名（例えば 'test'）
                    "status": friend['status'],
                    "request_sent_at": friend['request_sent_at'],
                    "approved_at": friend['approved_at']
                }
			friends_data.append(tmp)
		response_data = {
    		"friends": friends_data,
    		"total": friends.count()
		}
		return Response(response_data, status=HTTP_200_OK)

class FriendRequestView(APIView):
	'''
	各ユーザのステータス
	from_user		to_user

	null			null
	pending 		null
	null			pending
	pending			pending
	pending			approved
	approved		pending
	approved		approved
	で条件分岐
	'''
	def post(self, _, user_id):
		user_id_validator = UserIdValidator(data={"user_id": user_id})
		if not user_id_validator.is_valid():
			return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)
		
		to_user_id = int(user_id_validator.validated_data["user_id"])
		from_user_id = 1
		friend = Friends.objects.filter(from_user_id = from_user_id, to_user_id = to_user_id).first()
		rev_friend = Friends.objects.filter(from_user_id = to_user_id, to_user_id = from_user_id).first()
		# is_friend = Friends.objects.filter(from_user_id = from_user_id, to_user_id = to_user_id).exists()
		# friend_status = friend.status
		if friend or rev_friend:
			friend_status = friend.status if friend else None
			rev_friend_status = rev_friend.status if rev_friend else None

			if friend_status == "pending":
				return Response ({"error": "Friend request already sent."}, status=HTTP_409_CONFLICT)
			if friend_status == "approved" or rev_friend_status == "approved":#すでにfriend
				return Response ({"error": "Already friend."}, status=HTTP_400_BAD_REQUEST)
			if rev_friend_status == "pending":
				return  Response ({"error": "Friend requests have already been received."}, status=HTTP_409_CONFLICT)
		if from_user_id == to_user_id:
			return Response ({"error": "You cannot send a request to yourself."}, status=HTTP_400_BAD_REQUEST)
		
		Friends.objects.create(from_user_id = from_user_id, to_user_id = to_user_id, status = "pending")
		# patchのテストで使用
		Friends.objects.create(from_user_id = 100, to_user_id = 1, status = "pending")
		#
		return Response({"message": "Friend request sent successfully."}, status=HTTP_201_CREATED)

	def delete(self, _, user_id):
		user_id_validator = UserIdValidator(data={"user_id": user_id})
		if not user_id_validator.is_valid():
			return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)
		to_user_id = int(user_id_validator.validated_data["user_id"])
		from_user_id = 1
		#TODO
		if from_user_id == to_user_id:
			return Response ({"error": "You cannot send a request to yourself."}, status=HTTP_400_BAD_REQUEST)
		friend = Friends.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).first()
		rev_friend = Friends.objects.filter(from_user_id=to_user_id, to_user_id=from_user_id).first()
		if not friend:
			return Response({ "error": "No friend request exists from the specified user."}, status=HTTP_404_NOT_FOUND)
		if friend.status == "pending":
			Friends.objects.filter(from_user_id = from_user_id, to_user_id = to_user_id).delete()
			return Response(status=HTTP_204_NO_CONTENT)
		else:
			return Response ({"error": "Already friend."}, status=HTTP_400_BAD_REQUEST)#すでにfriend
		
	def patch(self, _, user_id):
		my_user_id = 1
		user_id_validator = UserIdValidator(data={"user_id": user_id})
		if not user_id_validator.is_valid():
			return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)
		from_user_id = int(user_id_validator.validated_data["user_id"])
		to_user_id = my_user_id

		if from_user_id == to_user_id:
			return Response ({"error": "You cannot send a request to yourself."}, status=HTTP_400_BAD_REQUEST)
		friend = Friends.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).first()
		if not friend:
			return Response({"error": "Friend request not found."}, status=HTTP_404_NOT_FOUND)
		friend_status = friend.status
		if friend_status == "approved":
			return Response({"error": "Friend request already approved."}, status=HTTP_409_CONFLICT)
		friend.status = "approved"
		friend.approved_at = now()
		friend.save()
		return Response({"userId":from_user_id}, status=HTTP_200_OK)
	
class	FriendView(APIView):
	def delete(self, _, friend_id):
		friend_id_validator = UserIdValidator(data={"user_id": friend_id})
		if not friend_id_validator.is_valid():
			return Response(friend_id_validator.errors, status=HTTP_400_BAD_REQUEST)
		to_user_id = int(friend_id_validator.validated_data["user_id"])
		from_user_id = 1
		if from_user_id == to_user_id:
			return Response ({"error": "You cannot send a request to yourself."}, status=HTTP_400_BAD_REQUEST)
		
		friend = Friends.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).first()
		rev_friend = Friends.objects.filter(from_user_id = to_user_id, to_user_id = from_user_id).first()
		if not friend and not rev_friend:
			return Response({"error": "Friend not found."}, status=HTTP_404_NOT_FOUND)
		if friend and friend.status == "approved":
			friend.delete()
		elif rev_friend and rev_friend.status == "approved":
			rev_friend.delete()
		else:
			return Response({"error": "Friend not found."}, status=HTTP_404_NOT_FOUND)
		return Response(status=HTTP_204_NO_CONTENT)
	