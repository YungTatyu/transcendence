import logging
import jwt

logger = logging.getLogger(__name__)


class JWTAuthMiddleware:
    """WebSocket のリクエストから JWT を取得し、検証する"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        logger.debug("starting to build ws connection")
        token = scope.get("cookies", {}).get("access_token")
        logger.debug(f"access token: {token}")

        if token is None:
            await send({"type": "websocket.close", "code": 1008})
            return

        try:
            decoded_token = jwt.decode(
                token, options={"verify_signature": False}, algorithms=["HS256"]
            )
            scope["user_id"] = str(decoded_token.get("user_id"))
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
            await send({"type": "websocket.close", "code": 1008})
            logger.warn("jwt auth failed")
            return

        logger.debug("jwt auth success")
        return await self.inner(scope, receive, send)
