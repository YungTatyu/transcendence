from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    KEY_MATCH_ID = "matchId"
    KEY_USERS = "userIdList"
    """
    以下の変数名は、requestのkeyの命名と完全に一致している必要がある
    """

    matchId = serializers.IntegerField(min_value=0, required=True)  # noqa: N815
    userIdList = serializers.ListField(  # noqa: N815
        child=serializers.IntegerField(min_value=0),
        min_length=1,
        required=True,
    )

    def validate_matchId(self, value):  # noqa: N802
        return value

    def validate_userIdList(self, users):  # noqa: N802
        # userの重複チェック
        if len(users) != len(set(users)):
            raise serializers.ValidationError("Duplicated user in a list.")
        return users
