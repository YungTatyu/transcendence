import logging

import requests
from game_app.settings import CA_CERT, MATCH_SERVICE
from client.vault_client import VaultClient

logger = logging.getLogger(__name__)


class MatchApiClient:
    @staticmethod
    def send_game_result(data):
        url = f"{MATCH_SERVICE}/matches/finish"
        try:
            api_key = VaultClient.fetch_api_key_not_required_token("matches")
            if api_key is None:
                raise ValueError("API key is missing")
            headers = {"X-API-KEY": api_key}
            response = requests.post(url, json=data, headers=headers, verify=CA_CERT)

            if response.status_code >= 400:
                error_detail = response.json()
                logger.critical(
                    f"POST {url}\n"
                    f"status: {response.status_code}\n"
                    f"respones: {error_detail}\n"
                    f"Sent Data: {data}"
                )
        except Exception as e:
            logger.critical(f"POST {url}\nSent Data: {data}\nerror: {e}")
