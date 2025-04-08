import base64
from datetime import date
import datetime
import json
import logging
from typing import Union

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    dsa,
    ec,
    ed448,
    ed25519,
    padding,
    rsa,
)
import jwt
from client.valut_client import VaultClient

# 公開鍵のインターフェース
PublicKeyType = Union[
    rsa.RSAPublicKey,
    dsa.DSAPublicKey,
    ec.EllipticCurvePublicKey,
    ed25519.Ed25519PublicKey,
    ed448.Ed448PublicKey,
]

logger = logging.getLogger(__name__)


def base64url_encode(data):
    """
    Base64Urlエンコード関数
    JWTの仕様(RFC 7519)上、'+','/','='を使用できないため置換
    """
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def create_unsigned_jwt(jwt_header: dict, jwt_payload: dict) -> bytes:
    """
    headerとpayloadをエンコードしたバイナリデータを作成
    """
    encoded_header = base64url_encode(json.dumps(jwt_header).encode())
    encoded_payload = base64url_encode(json.dumps(jwt_payload).encode())
    unsigned_jwt = encoded_header + b"." + encoded_payload
    return unsigned_jwt


def verify_jwt(pubkey: PublicKeyType, unsigned_jwt: bytes, signature: bytes) -> bool:
    """
    :param pubkey: 公開鍵オブジェクト
    :param unsigned_jwt: JWTのheaderとpayloadをエンコードしたバイナリデータ
    :param signature: JWTの署名

    True if (Success Verify JWT) else False
    """
    try:
        pubkey.verify(
            signature,
            unsigned_jwt,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception as e:
        logger.warn(str(e))
        return False


def extract_signature_from_jwt(signed_jwt: str) -> bytes:
    """
    JWT の "header.payload.signature" 形式の文字列から署名部分を抽出し、
    Base64 URL セーフデコードして bytes 型で返します。

    Args:
        signed_jwt (str): 完全な JWT トークン

    Returns:
        bytes: 署名部分をデコードしたバイナリデータ

    Raises:
        ValueError: JWT の形式が不正な場合
    """
    parts = signed_jwt.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format. Expected 'header.payload.signature'.")

    signature_b64 = parts[2]
    missing_padding = len(signature_b64) % 4
    if missing_padding:
        signature_b64 += "=" * (4 - missing_padding)

    return base64.urlsafe_b64decode(signature_b64)


def verify_signed_jwt(signed_jwt: str):
    token = VaultClient.fetch_token()
    if not token:
        logger.error("Failed to fetch token from Vault")
        return False

    extracted_signature = extract_signature_from_jwt(signed_jwt)
    pubkey = VaultClient.fetch_pubkey(token)

    if not extracted_signature or not pubkey:
        logger.error("failed to fetch extracted_signature or pubkey")
        return False
    # JWT を分割して header.payload 部分を取得
    try:
        parts = signed_jwt.split(".")
        if len(parts) != 3:
            raise ValueError(
                "Invalid JWT format: should contain 3 parts (header.payload.signature)"
            )

        unsigned_jwt = f"{parts[0]}.{parts[1]}".encode()  # header.payload 部分
    except Exception as e:
        logger.error(f"Error splitting signed JWT: {str(e)}")
        return False

    if not verify_jwt(pubkey, unsigned_jwt, extracted_signature):
        logger.error("JWT is invalid")
        return False

    try:
        payload = jwt.decode(signed_jwt, options={"verify_signature": False})
        exp = payload.get("exp")
        if exp is None:
            logger.error("JWT does not contain an 'exp' claim")
            return False

        if datetime.datetime.utcnow().timestamp() > exp:
            logger.error("JWT has expired")
            return False

    except jwt.DecodeError:
        logger.error("Failed to decode JWT")
        return False
    except jwt.ExpiredSignatureError:
        logger.error("JWT has expired")
        return False

    return True
