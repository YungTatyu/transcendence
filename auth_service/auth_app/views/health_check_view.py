from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        """
        ヘルスチェック用エンドポイント
        """
        return JsonResponse({"status": "healthy"}, status=200)
