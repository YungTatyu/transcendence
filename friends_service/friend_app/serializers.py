from rest_framework import serializers

from .models import Friend




class UserIdValidator(serializers.Serializer):
    user_id = serializers.CharField()

    def validate_user_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("UserID is invalid")
        return value


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"

class FriendQuerySerializer(serializers.Serializer):
    DEFAULT_OFFSET = 0
    DEFAULT_LIMIT = 20
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    SERIALIZE_CHOICES = [(STATUS_PENDING, "pending"), (STATUS_APPROVED, "approved")]

    status = serializers.ChoiceField(choices=SERIALIZE_CHOICES,required=False)
    offset = serializers.IntegerField(min_value=0, required=False, default=DEFAULT_OFFSET)
    limit = serializers.IntegerField(min_value=1, required=False, default=DEFAULT_LIMIT)
