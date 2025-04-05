import base64
import logging
from typing import Optional

import requests
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from .jwt_utils import PublicKeyType, create_unsigned_jwt, verify_jwt

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
