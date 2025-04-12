import logging
import ssl

import aiohttp
from config.settings import CA_CERT
from match_app.client.vault_client import VaultClient

logger = logging.getLogger(__name__)


class GameClient:
    def __init__(self, base_url):
        """
        :param base_url: The base URL of the API (e.g., http://localhost:80)
        """
        self.base_url = base_url

    async def fetch_games(self, match_id: int, user_ids: list[int]) -> dict:
        """
        非同期でGameAPIの/gamesエンドポイントを叩き、Jsonデータを返す
        ネットワークエラー等の場合、{"error": "Internal Server Error"}を返す
        """
        endpoint = "games"
        url = f"{self.base_url}/{endpoint}"

        body = {
            "matchId": match_id,
            "userIdList": user_ids,
        }

        api_key = VaultClient.fetch_api_key_not_required_token("games")
        if api_key is None:
            return {"error": "Internal Server Error"}
        headers = {"X-API-KEY": api_key}

        try:
            ssl_context = ssl.create_default_context()
            ssl_context.load_verify_locations(CA_CERT)
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with (
                aiohttp.ClientSession(connector=connector) as session,
                session.post(url, json=body, headers=headers, timeout=5) as response,
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
