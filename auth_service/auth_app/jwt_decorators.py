from functools import wraps

import jwt
from django.http import JsonResponse


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return JsonResponse({"error": "Access token missing"}, status=401)

        try:
            # TODO 署名検証なしでデコード
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            request.user_id = decoded_token.get("user_id")  # user_id をリクエストに保存
            return func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

    return wrapper
