from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(write_only=True)
    to_user = serializers.CharField(write_only=True)
    from_user_id = serializers.PrimaryKeyRelatedField(
        source="from_user", read_only=True
    )
    to_user_id = serializers.PrimaryKeyRelatedField(source="to_user", read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["from_user", "to_user", "status", "from_user_id", "to_user_id"]

    def validate(self, attrs):
        from_user = attrs.get("from_user")
        to_user = attrs.get("to_user")

        # Check that both users exist
        try:
            from_user_obj = User.objects.get(username=from_user)
        except User.DoesNotExist:
            raise serializers.ValidationError({"from_user": "User not found."})

        try:
            to_user_obj = User.objects.get(username=to_user)
        except User.DoesNotExist:
            raise serializers.ValidationError({"to_user": "User not found."})

        # Prevent self-referential friend requests
        if from_user == to_user:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself."
            )

        # Add user objects to validated data
        attrs["from_user"] = from_user_obj
        attrs["to_user"] = to_user_obj

        return attrs
