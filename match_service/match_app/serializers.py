from rest_framework import serializers


class MatchHistorySerializer(serializers.Serializer):
    # INFO docs/matches.ymlで/matches/histories/エンドポイントのlimitのdefault値は10と定義しています
    DEFAULT_LIMIT = 10
    # INFO docs/matches.ymlで/matches/histories/エンドポイントのlimitのmax値は100と定義しています
    MAX_LIMIT = 100
    # INFO docs/matches.ymlで/matches/histories/エンドポイントのoffsetのdefault値は0と定義しています
    DEFAULT_OFFSET = 0

    offset = serializers.IntegerField(
        min_value=0, required=False, default=DEFAULT_OFFSET
    )
    limit = serializers.IntegerField(
        min_value=1, max_value=MAX_LIMIT, required=False, default=DEFAULT_LIMIT
    )


class MatchSerializer(serializers.Serializer):
    # INFO docs/matches.ymlで/matches/エンドポイントのlimitのdefault値は10と定義しています
    DEFAULT_LIMIT = 10
    # INFO docs/matches.ymlで/matches/エンドポイントのlimitのmax値は100と定義しています
    MAX_LIMIT = 100
    # INFO docs/matches.ymlで/matches/エンドポイントのoffsetのdefault値は0と定義しています
    DEFAULT_OFFSET = 0

    matchId = serializers.IntegerField(min_value=0, required=False)  # noqa: N815
    winnerUserId = serializers.IntegerField(min_value=0, required=False)  # noqa: N815
    mode = serializers.ChoiceField(choices=["QuickPlay", "Tournament"], required=False)
    tournamentId = serializers.IntegerField(min_value=0, required=False)  # noqa: N815
    round = serializers.IntegerField(min_value=1, required=False)
    offset = serializers.IntegerField(
        min_value=0, required=False, default=DEFAULT_OFFSET
    )
    limit = serializers.IntegerField(
        min_value=1, max_value=MAX_LIMIT, required=False, default=DEFAULT_LIMIT
    )


class UserIdValidator(serializers.Serializer):
    user_id = serializers.CharField()

    def validate_user_id(self, value):
        # user_id が数値であるかどうかをチェック
        if not value.isdigit():
            raise serializers.ValidationError("UserID is invalid")
        return value
