import datetime
import logging

import jwt
from client.vault_client import VaultClient
from utils.jwt_utils import (
    add_signature_to_jwt,
    create_unsigned_jwt,
    extract_signature_from_jwt,
    verify_jwt,
)

# INFO: test用に使用
JWT_HEADER = {"alg": "PS256", "typ": "JWT"}
JWT_EXPIRATION = 3600
REFRESH_TOKEN_EXPIRATION = 60 * 60 * 24 * 30

logger = logging.getLogger(__name__)


def generate_signed_jwt(user_id: str, expires_in: int = JWT_EXPIRATION):
    token = VaultClient.fetch_token()
    if not token:
        logger.error("Failed to fetch token from Vault")
        return None
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    jwt_payload = {
        "user_id": user_id,
        "exp": int(exp_time.timestamp()),
    }
    jwt_data = create_unsigned_jwt(JWT_HEADER, jwt_payload)
    signature = VaultClient.fetch_signature(token, jwt_data)
    if not signature:
        logger.error("Failed to fetch signature from Vault")
        return None
    signed_jwt = add_signature_to_jwt(jwt_data, signature)

    return signed_jwt


def generate_tokens(user_id: int):
    signed_jwt = generate_signed_jwt(str(user_id))
    if not signed_jwt:
        return None
    refresh_signed_jwt = generate_signed_jwt(str(user_id), REFRESH_TOKEN_EXPIRATION)
    if not refresh_signed_jwt:
        return None

    tokens = {
        "access": signed_jwt,
        "refresh": refresh_signed_jwt,
    }
    return tokens


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
