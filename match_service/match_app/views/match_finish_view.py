from match_app.models import Match
from match_app.serializers import MatchFinishSerializer
from match_app.utils.match_finish_service import MatchFinishService
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
from match_app.utils.apikey_decorators import apikey_required
from django.utils.decorators import method_decorator


class MatchFinishView(APIView):
    """試合終了時のトーナメントAPIへの通知とDBレコードの更新"""

    @method_decorator(apikey_required("matches"))
    def post(self, request):
        serializer = MatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        match_id: int = serializer.validated_data["matchId"]
        results: list[dict] = serializer.validated_data["results"]
        match = Match.objects.filter(match_id=match_id).first()

        finish_date = MatchFinishService.update_match_data(match_id, results)
        if match.mode == "Tournament":
            MatchFinishService.register_winner_in_parent_match(match, results)
            err_message = MatchFinishService.send_match_result_to_tournament(match)
            if err_message is not None:
                MatchFinishService.rollback_match_data(match_id, match, results)
                return Response(
                    {"error": err_message}, status=HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({"finishDate": str(finish_date)}, status=HTTP_200_OK)
