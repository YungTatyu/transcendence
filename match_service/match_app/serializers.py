from rest_framework import serializers


class TournamentMatchSerializer(serializers.Serializer):
    userIdList = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        allow_empty=True,  # 参加ユーザーが決まっていない試合は存在する
    )
    tournamentId = serializers.IntegerField(min_value=0)
    parentMatchId = serializers.IntegerField(min_value=0, allow_null=True)
    round = serializers.IntegerField(min_value=1)

    def validate_userIdList(self, value):
        # 重複するuserIdはエラーとする
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate user ID")
        return value


class MatchHistorySerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0, required=False, default=0)
    limit = serializers.IntegerField(min_value=1, required=False, default=10)
