import datetime
import logging

import jwt

from auth_app.client.jwt_utils import (
    add_signature_to_jwt,
    create_unsigned_jwt,
    extract_signature_from_jwt,
    verify_jwt,
)
from auth_app.client.vault_client import VaultClient
from auth_app.settings import (
    CA_CERT,
    CLIENT_CERT,
    CLIENT_KEY,
    JWT_EXPIRATION,
    JWT_HEADER,
    REFRESH_TOKEN_EXPIRATION,
    VAULT_ADDR,
)

logger = logging.getLogger(__name__)
client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)


def generate_signed_jwt(user_id: str, expires_in: int = JWT_EXPIRATION):
    token = client.fetch_token()
    if not token:
        logger.error("Failed to fetch token from Vault")
        return None
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    jwt_payload = {
        "user_id": user_id,
        "exp": int(exp_time.timestamp()),
    }
    jwt_data = create_unsigned_jwt(JWT_HEADER, jwt_payload)
    signature = client.fetch_signature(token, jwt_data)
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
    token = client.fetch_token()
    if not token:
        logger.error("Failed to fetch token from Vault")
        return False

    extracted_signature = extract_signature_from_jwt(signed_jwt)
    pubkey = client.fetch_pubkey(token)

    if not extracted_signature or not pubkey:
        return False

    if not verify_jwt(pubkey, signed_jwt, extracted_signature):
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

    return False
