from typing import Optional
import requests
import logging

logger = logging.getLogger(__name__)


class MatchClient:
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
            url, json=body, params=params, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response

    def create_tournament_match_record(
        self,
        user_id_list: list[int],
        tournament_id: int,
        parent_match_id: Optional[int],
        round: int,
    ):
        """
        /matches/tournament-matchを叩き、トーナメント試合レコードを作成
        エラーの場合INTERNAL_SERVER_ERRORを返す
        """
        endpoint = "matches/tournament-match"
        body = {
            "userIdList": user_id_list,
            "tournamentId": tournament_id,
            "parentMatchId": parent_match_id,
            "round": round,
        }
        try:
            return self.__send_request("POST", endpoint, body=body)
        except Exception as e:
            logger.error(
                f"Error occurred while create tournament match. "
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
