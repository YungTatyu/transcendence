import logging

import aiohttp

logger = logging.getLogger(__name__)


class GameClient:
    def __init__(self, base_url):
        """
        :param base_url: The base URL of the API (e.g., http://localhost:80)
        """
        self.base_url = base_url

    async def fetch_games(self, match_id: int, user_ids: list[int]):
        """ """
        endpoint = "games"
        url = f"{self.base_url}/{endpoint}"

        body = {
            "matchId": match_id,
            "userIdList": user_ids,
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
