# Create your views here.
from django.db.models import Q
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from .models import Friend
from .serializers import FriendSerializer, UserIdValidator, FriendQuerySerializer
from django.utils.decorators import method_decorator
from .jwt_decorators import jwt_required
from rest_framework.test import APIClient
import jwt
from rest_framework.decorators import api_view


class FriendListView(APIView):
    '''
    フレンド申請状態(pending)の時、クエリーのlimitsとフロントエンドの画面の関係から
    to_user_idが自身のユーザーID、from_user_idが自分以外のIDの時のみ表示する。
    '''
    @method_decorator(jwt_required)
    def get(self, request):
        query_serializer = FriendQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=HTTP_400_BAD_REQUEST)
        #jwtの対応
        user_id = request.user_id
        status = query_serializer.validated_data.get("status") 
        offset = query_serializer.validated_data.get("offset")
        limit = query_serializer.validated_data["limit"]
        if status == FriendQuerySerializer.STATUS_PENDING:
            friends = friends = Friend.objects.filter(Q(to_user_id=user_id) & Q(status = Friend.STATUS_PENDING))
        elif status == FriendQuerySerializer.STATUS_APPROVED:
            friends = friends = Friend.objects.filter((Q(from_user_id=user_id ) | Q(to_user_id=user_id)) & Q(status = Friend.STATUS_APPROVED))
        else:
            friends = Friend.objects.filter((Q(from_user_id=user_id) & Q(status=Friend.STATUS_APPROVED))| Q(to_user_id=user_id))
        friends_paginated = friends[offset: offset + limit]
        serializer = FriendSerializer(friends_paginated, many=True)
        friends_data = []
        for friend in serializer.data:
            friend_data = {
                "fromUserId": friend["from_user_id"],
                "toUserId": friend["to_user_id"],
                "status": friend["status"],
                "requestSentAt": friend["request_sent_at"],
                "approvedAt": friend["approved_at"],
            }
            friends_data.append(friend_data)
        response_data = {"friends": friends_data, "total": friends.count()}
        return Response(response_data, status=HTTP_200_OK)


class FriendRequestView(APIView):
    def __validate_friend_request(self, friend, rev_friend):
        friend_status = friend.status if friend else None
        rev_friend_status = rev_friend.status if rev_friend else None

        if friend_status == Friend.STATUS_PENDING:
            return Response(
                {"error": "Friend request already sent."}, status=HTTP_409_CONFLICT
            )
        if (
            friend_status == Friend.STATUS_APPROVED
            or rev_friend_status == Friend.STATUS_APPROVED
        ):  # すでにfriend
            return Response({"error": "Already friend."}, status=HTTP_400_BAD_REQUEST)
        if rev_friend_status == Friend.STATUS_PENDING:
            return Response(
                {"error": "Friend requests have already been received."},
                status=HTTP_409_CONFLICT,
            )
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(jwt_required)
    def post(self, request, user_id):
        user_id_validator = UserIdValidator(data={"user_id": user_id})
        if not user_id_validator.is_valid():
            return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)

        to_user_id = int(user_id_validator.validated_data["user_id"])
        #jwtの対応
        from_user_id = request.user_id
        friend = Friend.objects.filter(
            from_user_id=from_user_id, to_user_id=to_user_id
        ).first()
        """
        rev_friend:from_user_idとto_user_idを逆にしたもの
        """
        rev_friend = Friend.objects.filter(
            from_user_id=to_user_id, to_user_id=from_user_id
        ).first()

        if friend or rev_friend:
            return self.__validate_friend_request(friend, rev_friend)
        if from_user_id == to_user_id:
            return Response(
                {"error": "You cannot send a request to yourself."},
                status=HTTP_400_BAD_REQUEST,
            )

        Friend.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            status=Friend.STATUS_PENDING,
        )
        return Response(
            {"message": "Friend request sent successfully."}, status=HTTP_201_CREATED
        )

    @method_decorator(jwt_required)
    def delete(self, request, user_id):
        user_id_validator = UserIdValidator(data={"user_id": user_id})
        if not user_id_validator.is_valid():
            return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)
        to_user_id = int(user_id_validator.validated_data["user_id"])
        # jwtの対応
        from_user_id = request.user_id
        if from_user_id == to_user_id:
            return Response(
                {"error": "You cannot send a request to yourself."},
                status=HTTP_400_BAD_REQUEST,
            )
        friend = Friend.objects.filter(
            from_user_id=from_user_id, to_user_id=to_user_id
        ).first()
        if not friend:
            return Response(
                {"error": "No friend request exists from the specified user."},
                status=HTTP_404_NOT_FOUND,
            )
        if friend.status != Friend.STATUS_PENDING:
            return Response(
                {"error": "Already friend."}, status=HTTP_400_BAD_REQUEST
            )  # すでにfriend
        Friend.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @method_decorator(jwt_required)
    def patch(self, request, user_id):
        # jwtの対応
        my_user_id = request.user_id
        user_id_validator = UserIdValidator(data={"user_id": user_id})
        if not user_id_validator.is_valid():
            return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)
        from_user_id = int(user_id_validator.validated_data["user_id"])
        to_user_id = my_user_id

        if from_user_id == to_user_id:
            return Response(
                {"error": "You cannot send a request to yourself."},
                status=HTTP_400_BAD_REQUEST,
            )
        friend = Friend.objects.filter(
            from_user_id=from_user_id, to_user_id=to_user_id
        ).first()
        if not friend:
            return Response(
                {"error": "Friend request not found."}, status=HTTP_404_NOT_FOUND
            )
        if friend.status == Friend.STATUS_APPROVED:
            return Response(
                {"error": "Friend request already approved."}, status=HTTP_409_CONFLICT
            )
        friend.status = Friend.STATUS_APPROVED
        friend.approved_at = now()
        friend.save()
        return Response({"userId": from_user_id}, status=HTTP_200_OK)


class FriendView(APIView):
    @method_decorator(jwt_required)
    def delete(self, request, friend_id):
        friend_id_validator = UserIdValidator(data={"user_id": friend_id})
        if not friend_id_validator.is_valid():
            return Response(friend_id_validator.errors, status=HTTP_400_BAD_REQUEST)
        to_user_id = int(friend_id_validator.validated_data["user_id"])
        # jwtの対応
        from_user_id = request.user_id
        if from_user_id == to_user_id:
            return Response(
                {"error": "You cannot send a request to yourself."},
                status=HTTP_400_BAD_REQUEST,
            )

        friend = Friend.objects.filter(
            from_user_id=from_user_id, to_user_id=to_user_id
        ).first()
        rev_friend = Friend.objects.filter(
            from_user_id=to_user_id, to_user_id=from_user_id
        ).first()
        match (friend is not None, rev_friend is not None):
            case (True, False) if friend.status == Friend.STATUS_APPROVED:
                friend.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            case (False, True) if rev_friend.status == Friend.STATUS_APPROVED:
                rev_friend.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            case _:
                return Response(
                    {"error": "Friend not found."}, status=HTTP_404_NOT_FOUND
                )

@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)