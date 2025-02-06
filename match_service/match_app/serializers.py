from rest_framework import serializers


class MatchHistorySerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0, required=False, default=0)
    limit = serializers.IntegerField(
        min_value=1, max_value=100, required=False, default=10
    )


class MatchSerializer(serializers.Serializer):
    matchId = serializers.IntegerField(min_value=0, required=False)  # noqa: N815
    winnerUserId = serializers.IntegerField(min_value=0, required=False)  # noqa: N815
    mode = serializers.ChoiceField(choices=["QuickPlay", "Tournament"], required=False)
    tournamentId = serializers.IntegerField(min_value=0, required=False)  # noqa: N815
    round = serializers.IntegerField(min_value=1, required=False)
    offset = serializers.IntegerField(min_value=0, required=False, default=0)
    limit = serializers.IntegerField(
        min_value=1, max_value=100, required=False, default=10
    )


class UserIdValidator(serializers.Serializer):
    user_id = serializers.CharField()

    def validate_user_id(self, value):
        # user_id が数値であるかどうかをチェック
        if not value.isdigit():
            raise serializers.ValidationError("UserID is invalid")
        return value
