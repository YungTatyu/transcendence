from django.views.generic import DeleteView
from .models import User, Note
from .serializers import UserSerializer, NoteSerializer

from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # ユーザーを作成
        self.user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # トークンを発行
        token, created = Token.objects.get_or_create(user=self.user)

        # トークンとユーザー情報を返す
        return Response(
            {
                "token": token.key,
                "id": self.user.id,
                "username": self.user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        # リクエストユーザー自身のみ削除可能にする場合
        return self.queryset.filter(id=self.request.user.id)


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Note.objects.all().order_by("created_at")
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class NoteListView(ListAPIView):
    queryset = Note.objects.all().order_by("-created_at")
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]


class NoteDetailView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = "id"


class NoteCreateView(CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteUpdateView(UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        # 自分のノートのみ更新可能にする
        return self.queryset.filter(author=self.request.user)


class NoteDestroyView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        # リクエストユーザー自身のみ削除可能にする場合
        return self.queryset.filter(author=self.request.user)


class UserLoginView(APIView):
    """
    Custom login view to authenticate users and provide tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid credentials. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Generate or get the token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token and user information
        return Response(
            {
                "token": token.key,
                "id": user.id,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def post(self, request):
        # 現在の認証トークンを取得
        token = request.auth
        if token:
            token.delete()
        return Response({"detail": "Logged out successfully."}, status=204)