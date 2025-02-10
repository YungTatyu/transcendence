from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        """
        ヘルスチェック用エンドポイント
        """
        return Response({"status": "healthy"}, status=200)
