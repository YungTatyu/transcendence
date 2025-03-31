from functools import wraps

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from .vault_client import VaultClient


def apikey_required(
    api_name: str, vault_addr: str, client_cert: str, client_key: str, ca_cert: str
):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            api_key = request.headers.get("x-api-key")

            if not api_key:
                return Response(
                    {"error": "x-api-key is required"}, status=HTTP_401_UNAUTHORIZED
                )

            client = VaultClient(vault_addr, client_cert, client_key, ca_cert)
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


def apikey_fetcher(
    api_name: str, vault_addr: str, client_cert: str, client_key: str, ca_cert: str
):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            vault_client = VaultClient(vault_addr, client_cert, client_key, ca_cert)
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
