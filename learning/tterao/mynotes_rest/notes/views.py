from .models import User, Note
from rest_framework import permissions, viewsets
from .serializers import UserSerializer, NoteSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Note.objects.all().order_by("created_at")
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
