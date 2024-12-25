import base64
import json
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Vaultの設定
VAULT_ADDR = "http://127.0.0.1:8200"
VAULT_TOKEN = "root"
TRANSIT_KEY = "signing-key"

# JWTのヘッダーとペイロード
header = {
    "alg": "RS256",  # RSA SHA-256を使用
    "typ": "JWT"
}

payload = {
    "sub": "1234567890",
    "userId": "1",
}

# Base64Urlエンコード関数
def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=")

# 署名の元データ(JWTのヘッダとペイロードをBase64変換)
encoded_header = base64url_encode(json.dumps(header).encode())
encoded_payload = base64url_encode(json.dumps(payload).encode())
jwt_data = encoded_header + b"." + encoded_payload
b64_jwt_data = base64.b64encode(jwt_data).decode()

# Vaultで署名を生成
headers = {"X-Vault-Token": VAULT_TOKEN}
sign_url = f"{VAULT_ADDR}/v1/transit/sign/{TRANSIT_KEY}"
sign_request_data = {
    "input": b64_jwt_data
}

response = requests.post(sign_url, headers=headers, json=sign_request_data)
if response.status_code != 200:
    print("Vaultで署名エラー:", response.text)
    exit()
else:
    signature = response.json()["data"]["signature"]
    # signature_dataはJWTの署名部分
    signature_data = base64.b64decode(signature.split(":")[-1])

# Vaultから公開鍵を取得
key_url = f"{VAULT_ADDR}/v1/transit/keys/{TRANSIT_KEY}"
response = requests.get(key_url, headers=headers)
if response.status_code != 200:
    print("公開鍵取得エラー:", response.text)
    exit()
else:
    public_key_pem = response.json()["data"]["keys"]["1"]["public_key"]
    public_key = load_pem_public_key(public_key_pem.encode())

try:
    public_key.verify(
        # JWTの署名部分
        signature_data,
        # JWTのヘッダとペイロード部分
        jwt_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("署名の検証に成功しました！JWTが有効です。")
except Exception as e:
    print("署名の検証に失敗しました:", str(e))
    exit(1)
