from django.core.validators import MinLengthValidator
from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[MinLengthValidator(1)], max_length=10)


class UserDataSerializer(serializers.Serializer):
    userId = serializers.IntegerField( source="user_id")  # noqa: N815
    username = serializers.CharField(validators=[MinLengthValidator(1)], max_length=10)
    avatarPath = serializers.CharField(max_length=100, source="avatar_path")  # noqa: N815


class QueryParamSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=False, source="user_id")  # noqa: N815
    username = serializers.CharField(
        validators=[MinLengthValidator(1)], max_length=10, required=False
    )

    def validate(self, data):
        """
        `username` または `userid` のどちらか一方のみを許可するバリデーション
        """

        username = data.get("username")
        user_id = data.get("user_id")

        if username is None and user_id is None:
            raise serializers.ValidationError(
                "query parameter 'username' or 'userId' is required."
            )

        if username is not None and user_id is not None:
            raise serializers.ValidationError(
                "query parameter 'username' or 'userId' must not be provided together."
            )

        return data
