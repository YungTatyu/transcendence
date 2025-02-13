import base64
import json
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

# 公開鍵のインターフェース
PublicKeyType = Union[
    rsa.RSAPublicKey,
    dsa.DSAPublicKey,
    ec.EllipticCurvePublicKey,
    ed25519.Ed25519PublicKey,
    ed448.Ed448PublicKey,
]


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
        print(str(e))
        return False
