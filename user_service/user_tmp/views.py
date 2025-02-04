from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models  import User
from .serializers import createUserSerializer

class UserView(APIView):
    def post(self, request):
        serializer = createUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        if User.objects.filter(name="username").exists():
            return Response({"error": "User arledy exists"}, status=HTTP_409_CONFLICT)
        

        user = User.objects.create(username=username)

        data = {"userI": user.user_id, "username": user.username}

        return Response(data, status=HTTP_201_CREATED)


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    user serverが機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
