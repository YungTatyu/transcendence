import logging

import jwt
import datetime

from auth_app.client.jwt_utils import (
    add_signature_to_jwt,
    create_unsigned_jwt,
    extract_signature_from_jwt,
    verify_jwt,
)
from auth_app.client.vault_client import VaultClient
from auth_app.settings import CA_CERT, CLIENT_CERT, CLIENT_KEY, JWT_HEADER, VAULT_ADDR

logger = logging.getLogger(__name__)
client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)


def generate_signed_jwt(user_id: str, expires_in: int = 3600):
    token = client.fetch_token()
    if not token:
        logger.error("Failed to fetch token from Vault")
        return None
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    jwt_payload = {
        "userId": user_id,
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

    tokens = {
        "access": signed_jwt,
        "refresh": jwt.encode({"user_id": str(user_id)}, None, algorithm=None),
    }
    return tokens


def verify_signed_jwt(signed_jwt: str):
    token = client.fetch_token()
    if not token:
        logger.error("Failed to fetch token from Vault")
        return False

    extracted_signature = extract_signature_from_jwt(signed_jwt)
    pubkey = client.fetch_pubkey(token)

    if extracted_signature and pubkey:
        return verify_jwt(pubkey, signed_jwt, extracted_signature)

    return False
