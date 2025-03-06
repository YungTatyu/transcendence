from functools import wraps

import jwt
from rest_framework.response import Response


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return Response({"error": "Access token missing"}, status=401)

        try:
            # TODO 署名検証なしでデコード
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            request.user_id = decoded_token.get("user_id")  # user_id をリクエストに保存
            
            return func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=401)
        # request.user_id = 1

    return wrapper
