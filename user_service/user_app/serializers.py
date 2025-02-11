from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)


class UserDataSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=10)
    avatar_path = serializers.CharField(max_length=100)


class QueryParamSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=10, required=False)

    def validate(self, data):
        """
        `username` または `userid` のどちらか一方のみを許可するバリデーション
        """

        username = data.get("username")
        user_id = data.get("user_id")

        if not username and not user_id:
            raise serializers.ValidationError(
                "query parameter 'username' or 'userid' is required."
            )

        if username and user_id:
            raise serializers.ValidationError(
                "query parameter 'username' or 'userid' must not be provided together."
            )

        return data
