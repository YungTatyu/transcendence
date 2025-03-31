from functools import wraps

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from user_app.settings import VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT
from user_app.vault_client.vault_client import VaultClient


def apikey_required(api_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            api_key = request.headers.get("x-api-key")

            if not api_key:
                return Response(
                    {"error": "x-api-key is required"}, status=HTTP_401_UNAUTHORIZED
                )

            client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)
            is_verify = client.verify_api_key(api_key, api_name)
            if is_verify is None:
                return Response(
                    {"error": "Internal Server Error"},
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            if not is_verify:
                return Response(
                    {"error": "x-api-key is invalid"}, status=HTTP_401_UNAUTHORIZED
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
