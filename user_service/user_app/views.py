from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer, QueryParamSerializer, UserDataSerializer


class UserView(APIView):
    def post(self, request):
        # リクエストボディをシリアライズ
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        # 既存のユーザーがいるか確認
        username = serializer.validated_data["username"]
        if User.objects.filter(username=username).exists():
            return Response({"error": "User arledy exists"}, status=HTTP_409_CONFLICT)

        # user新規作成
        user = User.objects.create(username=username)
        # レスポンスデータ作成
        data = {"userId": user.user_id, "username": user.username}

        return Response(data, status=HTTP_201_CREATED)

    def get(self, request):
        # クエリパラメーターのvalidation
        serializer = QueryParamSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        username = validated_data.get("username")
        user_id = validated_data.get("user_id")

        # ユーザー検索
        user = None
        if username:
            user = User.objects.filter(username=username).first()
        elif user_id:
            user = User.objects.filter(user_id=user_id).first()

        if not user:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        # レスポンスのシリアライズ
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    user serverが機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
