from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.apikey_decorators import apikey_required

from core.match_manager import MatchManager
from core.serializers import GameSerializer


class GameView(APIView):
    @method_decorator(apikey_required("games"))
    def post(self, request):
        """
        match情報を登録する
        matchesサーバからのみ叩かれる
        matchesサーバはゲームを開始する前に必ずこのapiを叩く
        """
        serializer = GameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            MatchManager.create_match(
                data.get(GameSerializer.KEY_MATCH_ID),
                data.get(GameSerializer.KEY_USERS),
            )
        except ValueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_409_CONFLICT)
        return Response(
            data={"message": "Match registerd."}, status=status.HTTP_201_CREATED
        )


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    game serverが正常に機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
