from rest_framework import serializers
from .models import Matches


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

    def validate(self, attrs):
        """tournament_idとroundが同じ試合が存在するか"""
        tournament_id = attrs.get("tournamentId")
        round = attrs.get("round")
        if Matches.objects.filter(tournament_id=tournament_id, round=round).exists():
            raise serializers.ValidationError("Tournament match already exist")

        return attrs


class MatchHistorySerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0, required=False, default=0)
    limit = serializers.IntegerField(
        min_value=1, max_value=100, required=False, default=10
    )


class MatchFinishSerializer(serializers.Serializer):
    class ResultSerializer(serializers.Serializer):
        userId = serializers.IntegerField(min_value=0)
        score = serializers.IntegerField(min_value=0)

    matchId = serializers.IntegerField(min_value=0)
    results = serializers.ListField(child=ResultSerializer())

    def validate_results(self, value):
        if not value:
            raise serializers.ValidationError("Results cannot be empty.")
        return value


class MatchesSerializer(serializers.Serializer):
    matchId = serializers.IntegerField(min_value=0, required=False)
    winnerUserId = serializers.IntegerField(min_value=0, required=False)
    mode = serializers.ChoiceField(choices=["QuickPlay", "Tournament"], required=False)
    tournamentId = serializers.IntegerField(min_value=0, required=False)
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
