import logging

import jwt
from friends_activity_app.utils.jwt_service import verify_signed_jwt


logger = logging.getLogger(__name__)


class JWTAuthMiddleware:
    """WebSocket のリクエストから JWT を取得し、検証する"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        logger.debug("starting to establish ws connection")
        subprotocols = scope.get("subprotocols", [])
        subprotocol = subprotocols[0] if subprotocols else None
        token = subprotocols[1] if len(subprotocols) > 1 else None

        if not all([subprotocol, token]):
            await send({"type": "websocket.close", "code": 1008})
            logger.warn("bad request: missing subprotocol or token")
            return

        try:
            is_valid = verify_signed_jwt(token)
            if not is_valid:
                logger.error("invalid jwt")
                await send({"type": "websocket.close", "code": 1008})
                return
            decoded_token = jwt.decode(
                token, options={"verify_signature": False}, algorithms=["HS256"]
            )
            scope["subprotocol"] = subprotocol
            scope["user_id"] = str(decoded_token.get("user_id"))
        except Exception as e:
            logger.exception(f"JWT verification failed: {e}")
            await send({"type": "websocket.close", "code": 1008})
            return

        logger.debug("jwt verification success")
        return await self.inner(scope, receive, send)
