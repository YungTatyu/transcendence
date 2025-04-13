import logging

import requests
from config.settings import CA_CERT
from match_app.client.vault_client import VaultClient

logger = logging.getLogger(__name__)


class TournamentClient:
    def __init__(self, base_url):
        """
        :param base_url: The base URL of the API (e.g., http://localhost:80)
        """
        self.base_url = base_url

    def __send_request(
        self, method, endpoint, body=None, params=None, headers=None, timeout=10
    ):
        """
        :param method: (GET | POST | DELETE | PATCH | PUT)
        :param endpoint: リクエストを送信するPath
        :param body: ボディに入れるJsonデータ
        :param params: QueryStringに入れるDictデータ

        200番台以外 OR ネットワーク系のエラーの場合例外が発生
        """
        url = f"{self.base_url}/{endpoint}"

        http_methods = {
            "GET": requests.get,
            "POST": requests.post,
            "DELETE": requests.delete,
            "PATCH": requests.patch,
            "PUT": requests.put,
        }

        response = http_methods[method](
            url,
            json=body,
            params=params,
            headers=headers,
            timeout=timeout,
            verify=CA_CERT,
        )
        response.raise_for_status()
        return response

    def finish_match(self, tournament_id, round) -> requests.Response:
        """
        /tournaments/finish-matchを叩き、試合終了を通知
        エラーの場合INTERNAL_SERVER_ERRORを返す
        """
        endpoint = "tournaments/finish-match"
        body = {"tournamentId": tournament_id, "round": round}

        try:
            api_key = VaultClient.fetch_api_key_not_required_token("tournaments")
            if api_key is None:
                raise ValueError("API key is missing")
            headers = {"X-API-KEY": api_key}
            return self.__send_request("POST", endpoint, body, headers=headers)
        except Exception as e:
            logger.error(
                f"Error occurred while finishing match. "
                f"Exception: {str(e)} "
                f"Endpoint: {self.base_url}/{endpoint} "
                f"Request Body: {body}",
            )
            response = requests.Response()
            response.status_code = 500
            response._content = b'{"error": "Internal Server Error"}'
            response.headers["Content-Type"] = "application/json"
            response.request = requests.Request(
                "POST", f"{self.base_url}/{endpoint}"
            ).prepare()
            return response
