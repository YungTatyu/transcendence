import logging
from typing import Optional

import aiohttp
import requests

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

    def fetch_matches_data(self, tournament_id: int, offset: int = 0, limit: int = 100):
        """
        /matchesを叩き、トーナメントIDに紐づくMatches情報を取得
        エラーの場合INTERNAL_SERVER_ERRORを返す
        INFO 引数のlimitはmatchesエンドポイントの最大レコード取得数に合わせています
        """
        endpoint = "matches"

        params = {
            "tournamentId": tournament_id,
            "offset": offset,
            "limit": limit,
        }

        try:
            return self.__send_request("GET", endpoint, params=params)
        except Exception as e:
            logger.error(
                f"Error occurred while get tournament matches. "
                f"Exception: {str(e)} "
                f"Endpoint: {self.base_url}/{endpoint} "
                f"Request params: {params}",
            )
            response = requests.Response()
            response.status_code = 500
            response._content = b'{"error": "Internal Server Error"}'
            response.headers["Content-Type"] = "application/json"
            response.request = requests.Request(
                "GET", f"{self.base_url}/{endpoint}"
            ).prepare()
            return response

    async def fetch_tournament_match_finish(self, match_id: int, results: list[dict]):
        """
        /matches/finishを叩き、トーナメント試合終了処理を行う
        エラーの場合{"error": "Internal Server Error"}を返す

        INFO MatchAPIを叩いた後、MatchAPI側がTournamentAPIのエンドポイントを叩きます。
             その時、MatchAPIを叩く処理が同期処理だと、MatchAPIから叩かれた時、
             TournamentAPIがブロッキングされていてデッドロック状態になるため、
             非同期でMatchAPIを叩きます。

             TournamentAPI ──> MatchAPI (同期リクエスト)
             TournamentAPI <── MatchAPI (同期リクエスト)   <== デッドロック状態

             TournamentAPI ──> MatchAPI (非同期リクエスト)
             TournamentAPI <── MatchAPI (同期リクエスト)   <== デッドロックしない
        """
        endpoint = "matches/finish"
        url = f"{self.base_url}/{endpoint}"

        body = {
            "matchId": match_id,
            "results": results,
        }

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.post(url, json=body, timeout=5) as response,
            ):
                return await response.json()
        except Exception as e:
            logger.error(
                f"Error occurred while finish tournament matches. "
                f"Exception: {str(e)} "
                f"Endpoint: {self.base_url}/{endpoint} "
                f"Request body: {body}",
            )
            return {"error": "Internal Server Error"}
