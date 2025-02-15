from rest_framework import serializers

from .models import Tournament
from .utils.tournament_session import TournamentSession


class TournamentMatchFinishSerializer(serializers.Serializer):
    tournamentId = serializers.IntegerField(min_value=0)  # noqa: N815
    round = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        """リクエストの内容とサーバ内の情報との整合性のチェック"""
        tournament_id = attrs.get("tournamentId")
        round = attrs.get("round")

        tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
        if tournament is None:
            raise serializers.ValidationError("The Tournament does not exist")
        if tournament.finish_date is not None:
            raise serializers.ValidationError("The Tournament is already over")

        tournament_session = TournamentSession.search(tournament_id)
        if tournament_session is None:
            raise serializers.ValidationError("The Tournament Session does not exist")
        if tournament_session.current_round != round:
            raise serializers.ValidationError("Mismatch with tournament session info")

        return attrs
