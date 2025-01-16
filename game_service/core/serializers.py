from enum import Enum
from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    class Keys(Enum):
        KEY_MATCH_ID = "matchId"
        KEY_USERS = "userIdList"

    match_id = serializers.IntegerField(
        min_value=0, required=True, source=Keys.KEY_MATCH_ID.value
    )
    users = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        min_length=1,
        required=True,
        source=Keys.KEY_USERS.value,
    )

    def validate_match_id(self, value):
        # TODO: match_idがmatchサービスに存在するか確認必要？
        return value

    def validate_users(self, users):
        # TODO: userが存在するか確認必要？
        return users
