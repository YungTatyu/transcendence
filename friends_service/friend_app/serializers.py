from rest_framework import serializers

from .models import Friends


class UserIdValidator(serializers.Serializer):
    user_id = serializers.CharField()

    def validate_user_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("UserID is invalid")
        return value


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = "__all__"
