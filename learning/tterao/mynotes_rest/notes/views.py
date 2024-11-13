from django.views.generic import DeleteView
from .models import User, Note
from rest_framework import permissions, viewsets
from .serializers import UserSerializer, NoteSerializer
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
