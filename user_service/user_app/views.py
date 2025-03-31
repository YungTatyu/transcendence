import os

from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
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

from .jwt_decorators import jwt_required
from .models import User
from .serializers import (
    AvatarSerializer,
    CreateUserSerializer,
    QueryParamSerializer,
    UserDataSerializer,
    UsernameSerializer,
)
from user_app.vault_client.apikey_decorators import apikey_required


class UserView(APIView):
    @method_decorator(apikey_required("users"))
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
        """
        user情報を取得する
        """
        # クエリパラメーターのvalidation
        serializer = QueryParamSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        username = validated_data.get("username")
        user_id = validated_data.get("userid")

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


class UsernameView(APIView):
    @method_decorator(jwt_required)
    def put(self, request):
        """
        usernameを変更する
        """

        user_id = request.user_id

        user = User.objects.get(user_id=user_id)

        serializer = UsernameSerializer(instance=user, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_409_CONFLICT)

        updated_user = serializer.save()

        return Response({"username": updated_user.username}, status=HTTP_200_OK)


class AvatarView(APIView):
    @method_decorator(jwt_required)
    def put(self, request):
        """
        avatarをdefaultからカスタムに変更する
        すでにカスタムの場合は上書き保存する
        """
        user_id = request.user_id

        # User インスタンスを取得
        user = User.objects.get(user_id=user_id)

        # instance=user を渡して update()を使用可能に
        serializer = AvatarSerializer(
            instance=user, data=request.data, context={"user_id": user_id}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        updated_user = serializer.save()

        return Response(
            data={"avatarPath": updated_user.avatar_path.url}, status=HTTP_200_OK
        )

    @method_decorator(jwt_required)
    def delete(self, request):
        """
        設定してある画像ファイルを削除し、defaultのパスを設定する
        """

        user_id = request.user_id

        # User インスタンスを取得
        user = User.objects.get(user_id=user_id)

        # デフォルトアバターなら削除しない
        if user.avatar_path.name == User.DEFAULT_AVATAR_PATH:
            return Response({"error": "Avatar not found."}, status=HTTP_404_NOT_FOUND)

        # ファイルのパスを取得して削除
        avatar_path = user.avatar_path.path
        if os.path.exists(avatar_path):
            default_storage.delete(avatar_path)

        # defaultのパスを設定
        user.avatar_path = User.DEFAULT_AVATAR_PATH
        user.save()

        return Response(status=HTTP_200_OK)


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    user serverが機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
