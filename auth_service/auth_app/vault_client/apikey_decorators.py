from functools import wraps

from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from auth_app.settings import VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT
from auth_app.vault_client.vault_client import VaultClient


def apikey_fetcher(api_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            vault_client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)
            token = vault_client.fetch_token()
            if token is None:
                return Response(
                    {"error": "Internal Server Error"},
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )

            api_keys = vault_client.fetch_api_key(token, api_name)
            if api_keys is None:
                return Response(
                    {"error": "Internal Server Error"},
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # APIキーとVaultトークンをセット
            request.api_key = api_keys["value"]
            request.token = token

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
