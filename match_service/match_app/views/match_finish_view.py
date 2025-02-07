from typing import Optional
import requests
from requests.exceptions import RequestException
from django.conf import settings
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from match_app.models import Match, MatchParticipant
from match_app.serializers import MatchFinishSerializer


class MatchFinishView(APIView):
    """試合終了時のトーナメントAPIへの通知とDBレコードの更新"""

    def post(self, request):
        serializer = MatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        match_id: int = serializer.validated_data["matchId"]
        results: list[dict] = serializer.validated_data["results"]

        # 先にトーナメントAPIを叩く(整合性維持のため)
        errcode, message = self.__send_match_result_if_tournament_match(match_id)
        if errcode is not None:
            return Response({"error": message}, status=errcode)

        finish_date = self.__update_match_data(match_id, results)
        return Response({"finishDate": str(finish_date)}, status=HTTP_200_OK)

    def __update_match_data(self, match_id: int, results: list[dict]) -> now:
        # MatchParticipantのscoreをユーザーそれぞれに対して更新
        for result in results:
            user_id = result["userId"]
            score = result["score"]
            MatchParticipant.objects.filter(match_id=match_id, user_id=user_id).update(
                score=score
            )

        # Matchのwinner_user_idとfinish_dateを更新
        winner_user_id = max(results, key=lambda x: x["score"])["userId"]
        finish_date = now()
        Match.objects.filter(match_id=match_id).update(
            winner_user_id=winner_user_id, finish_date=finish_date
        )

        return finish_date

    def __send_match_result_if_tournament_match(
        self, match_id: int
    ) -> tuple[Optional[int], str]:
        """
        if (mode == Tournament):
            /tournaments/finish-matchを叩き、試合終了を通知
        else:
            何もしない
        """
        match = Match.objects.filter(match_id=match_id).first()
        # modeがTournament以外なら何もしない
        if match.mode != "Tournament":
            return (None, "")

        url = f"{settings.TOURNAMENT_API_BASE_URL}/tournaments/finish-match"
        payload = {"tournamentId": match.tournament_id, "round": match.round}

        try:
            response = requests.post(url, json=payload, timeout=10)
            #  HTTPステータスコードが200番台以外であれば例外を発生させる
            response.raise_for_status()
        except Exception as e:
            return HTTP_500_INTERNAL_SERVER_ERROR, str(e)
        return None, ""
