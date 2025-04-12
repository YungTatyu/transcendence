import base64
import logging
from typing import Optional

import requests
from config.settings import (
    CA_CERT,
    CLIENT_CERT,
    CLIENT_KEY,
    VAULT_ADDR,
)
from cryptography.hazmat.primitives.serialization import load_pem_public_key

logger = logging.getLogger(__name__)


class VaultClient:
    BASE_URL = VAULT_ADDR
    CERT = (CLIENT_CERT, CLIENT_KEY)
    CA_FILE = CA_CERT

    @staticmethod
    def fetch_token() -> Optional[str]:
        """
        TLSクライアント認証を用いてトークンを取得
        INFO response.json()["auth"]["lease_duration"]はトークンの期限が切れるまでの秒数
        """
        url = f"{VaultClient.BASE_URL}/v1/auth/cert/login"

        try:
            response = requests.post(
                url, cert=VaultClient.CERT, verify=VaultClient.CA_FILE
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch token error: {e}")
            return None

        token = response.json().get("auth", {}).get("client_token")
        return token

    @staticmethod
    def fetch_signature(token: str, unsigned_jwt: bytes):
        """トークンを用いて署名なしJWTデータから署名を作成"""
        url = f"{VaultClient.BASE_URL}/v1/transit/sign/jwt-key"
        headers = {"X-Vault-Token": token}  # Vaultトークンを指定するヘッダ
        b64_jwt_data = base64.b64encode(unsigned_jwt).decode()  # バイナリを文字列に変換
        body = {"input": b64_jwt_data}

        try:
            response = requests.post(
                url,
                json=body,
                headers=headers,
                cert=VaultClient.CERT,
                verify=VaultClient.CA_FILE,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch signature data error: {e}")
            return None

        signature_data = response.json()["data"]["signature"]
        signature = base64.b64decode(signature_data.split(":")[-1])
        return signature

    @staticmethod
    def fetch_pubkey(token: str) -> Optional[bytes]:
        """トークンを用いて最新の公開鍵を取得"""
        url = f"{VaultClient.BASE_URL}/v1/transit/keys/jwt-key"
        headers = {"X-Vault-Token": token}

        try:
            response = requests.get(
                url, headers=headers, cert=VaultClient.CERT, verify=VaultClient.CA_FILE
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

    @staticmethod
    def fetch_api_key(token: str, api_key_name: str) -> Optional[dict[str, str]]:
        """APIキーを取得(自動ローテーションするため、APIキーのDictを返す)"""
        url = f"{VaultClient.BASE_URL}/v1/kv/apikeys/{api_key_name}"
        headers = {"X-Vault-Token": token}

        try:
            response = requests.get(
                url, headers=headers, cert=VaultClient.CERT, verify=VaultClient.CA_FILE
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"fetch pubkey list error: {e}")
            return None

        return response.json()["data"]

    @staticmethod
    def verify_api_key(api_key: str, api_key_name) -> Optional[bool]:
        token = VaultClient.fetch_token()
        if token is None:
            return None

        api_keys = VaultClient.fetch_api_key(token, api_key_name)

        if api_keys is None:
            return None

        return api_key in api_keys.values()
