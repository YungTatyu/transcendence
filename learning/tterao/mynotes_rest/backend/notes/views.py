from django.views.generic import DeleteView
from .models import User, Note
from .serializers import UserSerializer, NoteSerializer

from django.contrib.auth import authenticate
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # リクエストユーザー自身のみ削除可能にする場合
        return self.queryset.filter(id=self.request.user.id)


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Note.objects.all().order_by("created_at")
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class NoteListView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]


class NoteCreateView(CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDestroyView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # リクエストユーザー自身のみ削除可能にする場合
        return self.queryset.filter(author=self.request.user)


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"post")
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        print(f"is valid")
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(f"{e}")
        # serializer.is_valid(raise_exception=True)
        print(f"valid data")
        user = serializer.validated_data["user"]
        print(f"user: {user}")
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
            }
        )


# class CustomAuthToken(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         password = request.data.get("password")
#
#         if not username or not password:
#             return Response(
#                 {"detail": "Username and password are required"}, status=400
#             )
#
#         print(f"username: {username} password: {password}")
#         user = authenticate(username=username, password=password)
#
#         print(f"user: {user}")
#         if user is None:
#             return Response(
#                 {"detail": "Unable to log in with provided credentials."}, status=401
#             )
#
#         token, created = Token.objects.get_or_create(user=user)
#         print(f"Token created: {created}, Token: {token.key}")
#         return Response(
#             {
#                 "token": token.key,
#                 "user_id": user.id,
#                 "username": user.username,
#             }
#         )
#


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # トークン削除
        return Response({"detail": "Logged out successfully."}, status=204)
