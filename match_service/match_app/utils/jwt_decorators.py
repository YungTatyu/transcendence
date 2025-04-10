import logging
from functools import wraps

import jwt
from match_app.utils.jwt_service import verify_signed_jwt
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return Response({"error": "Access token missing"}, status=401)

        try:
            is_valid = verify_signed_jwt(token)
            if not is_valid:
                return Response({"error": "Invalid or expired token"}, status=401)
        except Exception:
            logger.exception("JWT verification failed")
            return Response({"error": "Failed to verify token"}, status=401)

        try:
            # 検証済みなので署名検証をスキップ
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            request.user_id = decoded_token.get("user_id")
            return func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=401)

    return wrapper
