from rest_framework import serializers

from .models import Match, MatchParticipant


class TournamentMatchSerializer(serializers.Serializer):
    userIdList = serializers.ListField(  # noqa: N815
        child=serializers.IntegerField(min_value=0),
        allow_empty=True,  # 参加ユーザーが決まっていない試合は存在する
    )
    tournamentId = serializers.IntegerField(min_value=0)  # noqa: N815
    parentMatchId = serializers.IntegerField(min_value=0, allow_null=True)  # noqa: N815
    round = serializers.IntegerField(min_value=1)

    def validate_userIdList(self, value):  # noqa: N802
        # 重複するuserIdはエラーとする
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate user ID")
        return value

    def validate(self, attrs):
        """tournament_idとroundが同じ試合が存在するか"""
        tournament_id = attrs.get("tournamentId")
        round = attrs.get("round")
        if Match.objects.filter(tournament_id=tournament_id, round=round).exists():
            raise serializers.ValidationError("Tournament match already exist")

        return attrs

    def validate_parentMatchId(self, value):  # noqa: N802
        # parentMatchIdがnullでなく、parentMatchが存在しない場合はエラー
        if value is not None and Match.objects.filter(match_id=value).first() is None:
            raise serializers.ValidationError("The ParentMatch does not exist")

        return value


class MatchFinishSerializer(serializers.Serializer):
    class ResultSerializer(serializers.Serializer):
        userId = serializers.IntegerField(min_value=0)  # noqa: N815
        score = serializers.IntegerField(min_value=-1)

    matchId = serializers.IntegerField(min_value=0)  # noqa: N815
    results = serializers.ListField(child=ResultSerializer())

    def validate_results(self, value):
        if not value:
            raise serializers.ValidationError("Results cannot be empty.")

        scores = [result["score"] for result in value]
        winner_score = max(scores)
        # 勝者は１人か
        if scores.count(winner_score) != 1:
            raise serializers.ValidationError("There are multiple winner")

        request_user_ids = [result["userId"] for result in value]

        # リクエストデータのuser_idが重複していないか
        if len(request_user_ids) != len(set(request_user_ids)):
            raise serializers.ValidationError("There are multiple userId")

        return value

    def validate_matchId(self, value):  # noqa: N802
        match = Match.objects.filter(match_id=value).first()

        # 試合が存在するか
        if match is None:
            raise serializers.ValidationError("The match does not exist")
        # 試合終了の処理済みではないか
        if match.finish_date is not None:
            raise serializers.ValidationError("Match is already finished")

        return value

    def validate(self, attrs):
        # リクエストボディとDB内のuser_idsに整合性があるか
        match_id = attrs.get("matchId")
        results = attrs.get("results")
        request_user_ids = [result["userId"] for result in results]
        stored_user_ids = MatchParticipant.objects.filter(
            match_id=match_id
        ).values_list("user_id", flat=True)

        if set(request_user_ids) != set(stored_user_ids):
            raise serializers.ValidationError("Invalid user_ids")

        return attrs


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
