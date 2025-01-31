from functools import wraps

import jwt
from django.http import JsonResponse


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return JsonResponse(
                {"error": "Invalid Authorization header format"}, status=401
            )

        token = parts[1]

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
