from urllib.parse import parse_qs
import jwt
from channels.middleware.base import BaseMiddleware
from starlette.websockets import WebSocketDisconnect

class JWTAuthMiddleware(BaseMiddleware):
    """ WebSocketのリクエストからJWTを取得し、検証する """

    async def __call__(self, scope, receive, send):
        token = scope.get("cookies", {}).get("access_token")

        if token:
            try:
                decoded_token = jwt.decode(token, options={"verify_signature": False})
                scope["user_id"] = str(decoded_token.get("user_id"))
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                await send({
                    "type": "websocket.close",
                    "code": 1008
                })
                return
        else:
            await send({
                "type": "websocket.close",
                "code": 1008
            })
            return

        return await super().__call__(scope, receive, send)
