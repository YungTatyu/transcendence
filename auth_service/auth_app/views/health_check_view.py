from django.http import JsonResponse
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        """
        ヘルスチェック用エンドポイント
        """
        return JsonResponse({"status": "healthy"}, status=200)
