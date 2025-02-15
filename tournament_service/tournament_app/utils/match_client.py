from typing import Optional
import requests


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
        HTTPステータスコードが200番台以外であれば例が発生
        ネットワーク系のエラーの場合例外が発生
        """
        endpoint = "matches/tournament-match"
        body = {
            "userIdList": user_id_list,
            "tournamentId": tournament_id,
            "parentMatchId": parent_match_id,
            "round": round,
        }
        return self.__send_request("POST", endpoint, body)
