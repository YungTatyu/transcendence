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
from .serializers import CreateUserSerializer, SearchUserSerializer


class UserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        if User.objects.filter(username="username").exists():
            return Response({"error": "User arledy exists"}, status=HTTP_409_CONFLICT)

        user = User.objects.create(username=username)

        data = {"userId": user.user_id, "username": user.username}

        return Response(data, status=HTTP_201_CREATED)

    def get(self, request):
        username = request.GET.get("username")
        userid = request.GET.get("userid")

        if not username and not userid:
            return Response(
                {"error": "query parameter 'username' or 'userid' is required."},
                status=HTTP_400_BAD_REQUEST,
            )

        if username and userid:
            return Response(
                {"error": "query parameter 'username' or 'userid' is required."},
                status=HTTP_400_BAD_REQUEST,
            )

        if username:
            user = User.objects.filter(username=username).first()
        elif userid:
            user = User.objects.filter(user_id=userid).first()

        if not user:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        serializer = SearchUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    user serverが機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
