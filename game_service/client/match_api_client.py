import logging

import requests
from game_app.settings import MATCH_SERVICE, CA_CERT

logger = logging.getLogger(__name__)


class MatchApiClient:
    @staticmethod
    def send_game_result(data):
        url = f"{MATCH_SERVICE}/matches/finish"
        try:
            response = requests.post(url, json=data, verify=CA_CERT)

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
