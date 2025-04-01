import base64
import logging
from typing import Optional

import requests
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from jwt_utils import PublicKeyType, create_unsigned_jwt, verify_jwt

logger = logging.getLogger(__name__)


class VaultClient:
    def __init__(self, base_url, cert_file, key_file, ca_file):
        self.__base_url = base_url
        self.__cert = (cert_file, key_file)
        self.__ca_file = ca_file

    def fetch_token(self) -> Optional[str]:
        """
        TLSクライアント認証を用いてトークンを取得
        INFO response.json()["auth"]["lease_duration"]はトークンの期限が切れるまでの秒数
        """
        url = f"{self.__base_url}/v1/auth/cert/login"

        try:
            response = requests.post(url, cert=self.__cert, verify=self.__ca_file)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch token error: {e}")
            return None

        token = response.json().get("auth", {}).get("client_token")
        return token

    def fetch_signature(
        self, token: str, unsigned_jwt: bytes
    ) -> Optional[PublicKeyType]:
        """トークンを用いて署名なしJWTデータから署名を作成"""
        url = f"{self.__base_url}/v1/transit/sign/jwt-key"
        headers = {"X-Vault-Token": token}  # Vaultトークンを指定するヘッダ
        b64_jwt_data = base64.b64encode(unsigned_jwt).decode()  # バイナリを文字列に変換
        body = {"input": b64_jwt_data}

        try:
            response = requests.post(
                url, json=body, headers=headers, cert=self.__cert, verify=self.__ca_file
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch signature data error: {e}")
            return None

        signature_data = response.json()["data"]["signature"]
        signature = base64.b64decode(signature_data.split(":")[-1])
        return signature

    def fetch_pubkey(self, token: str) -> Optional[bytes]:
        """トークンを用いて最新の公開鍵を取得"""
        url = f"{self.__base_url}/v1/transit/keys/jwt-key"
        headers = {"X-Vault-Token": token}

        try:
            response = requests.get(
                url, headers=headers, cert=self.__cert, verify=self.__ca_file
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch pubkey list error: {e}")
            return None

        keys_dict = response.json()["data"]["keys"]
        latest_version = max(map(int, keys_dict.keys()))  # 最新の公開鍵の番号
        pubkey_pem = keys_dict[str(latest_version)]["public_key"]
        pubkey = load_pem_public_key(pubkey_pem.encode())
        return pubkey

    def fetch_api_key(self, token: str, api_key_name: str) -> Optional[dict[str, int]]:
        """APIキーを取得(自動ローテーションするため、APIキーのDictを返す)"""
        url = f"{self.__base_url}/v1/kv/apikeys/{api_key_name}"
        headers = {"X-Vault-Token": token}

        try:
            response = requests.get(
                url, headers=headers, cert=self.__cert, verify=self.__ca_file
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch pubkey list error: {e}")
            return None

        return response.json()["data"]


if __name__ == "__main__":
    # INFO localhostからvaultAPIを叩く場合、CNの設定上、
    #      "/etc/hostsファイルに127.0.0.1 vault" を追加する必要がある
    VAULT_ADDR = "https://vault:8200"
    CLIENT_CERT = "../../certs/client.crt"
    CLIENT_KEY = "../../certs/client.key"
    CA_CERT = "../../certs/ca.crt"

    client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)
    # INFO tokenは一定期間同じものを使用できます
    token = client.fetch_token()
    if token:
        jwt_header = {"alg": "RS256", "typ": "JWT"}
        jwt_payload = {"userId": "1"}
        jwt_data = create_unsigned_jwt(jwt_header, jwt_payload)
        signature = client.fetch_signature(token, jwt_data)
        pubkey = client.fetch_pubkey(token)
        if signature and pubkey:
            print("Verify JWT: ", verify_jwt(pubkey, jwt_data, signature))

        users_apikeys = client.fetch_api_key(token, "users")
        matches_apikeys = client.fetch_api_key(token, "matches")
        tournaments_apikeys = client.fetch_api_key(token, "tournaments")
        games_apikeys = client.fetch_api_key(token, "games")
        print("APIKEY[users]: ", users_apikeys)
        print("APIKEY[matches]: ", matches_apikeys)
        print("APIKEY[tournaments]: ", tournaments_apikeys)
        print("APIKEY[games]: ", games_apikeys)
