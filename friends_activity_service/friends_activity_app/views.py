from django.http import JsonResponse

def health_check(request):
    """
    ヘルスチェック用エンドポイント。
    dockerコンテナの起動時などに利用可能。
    """
    return JsonResponse({"status": "healthy"})
