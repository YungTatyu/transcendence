from rest_framework import serializers
from .models import User, Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "author"]

    def create(self, validated_data):
        user = self.context["request"].user
        note = Note(
            title=validated_data["title"],
            content=validated_data["content"],
            author=user,
        )
        note.save()
        return note
