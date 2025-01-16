from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GameView(APIView):
    def post(self, request):
        """
        match情報を登録する
        matchesサーバからのみ叩かれる
        matchesサーバはゲームを開始する前に必ずこのapiを叩く
        """
        pass


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    game serverが正常に機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
