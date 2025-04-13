from functools import wraps

from client.vault_client import VaultClient
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR


def apikey_required(api_name: str):
    """
    APIキーを受け取る側のサーバ用のデコレータ
    APIキー認証でエラーとなる場合、エラーレスポンスが返る
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            api_key = request.headers.get("x-api-key")

            if not api_key:
                return Response(
                    {"error": "x-api-key is required"}, status=HTTP_401_UNAUTHORIZED
                )

            is_verify = VaultClient.verify_api_key(api_key, api_name)
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


def apikey_fetcher(api_name: str):
    """
    APIキーを送信する側のサーバ用デコレータ
    requestにAPIキーとVaultトークンをセットする
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            token = VaultClient.fetch_token()
            if token is None:
                return Response(
                    {"error": "Internal Server Error"},
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )

            api_keys = VaultClient.fetch_api_key(token, api_name)
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
