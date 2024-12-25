import base64
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

VAULT_ADDR = "http://127.0.0.1:8200"
VAULT_TOKEN = "root"
TRANSIT_KEY = "signing-key"
PAYLOAD = "ABC"

# vaultのエンドポイントがbase64エンコード済みの文字列を要求するため
encoded_payload = base64.b64encode(PAYLOAD.encode()).decode()

headers = {"X-Vault-Token": VAULT_TOKEN}
sign_url = f"{VAULT_ADDR}/v1/transit/sign/{TRANSIT_KEY}"
sign_request_data = {
    "input": encoded_payload,
    "key_version": 1
}

response = requests.post(sign_url, headers=headers, json=sign_request_data)
if response.status_code != 200:
    print("Vaultで署名エラー:", response.text)
    exit()
else:
    signature = response.json()["data"]["signature"]

key_url = f"{VAULT_ADDR}/v1/transit/keys/{TRANSIT_KEY}"
response = requests.get(key_url, headers=headers)
if response.status_code != 200:
    print("公開鍵取得エラー:", response.text)
    exit()
else:
    public_key_pem = response.json()["data"]["keys"]["1"]["public_key"]

# 公開鍵をPEM形式で読み込み
public_key = load_pem_public_key(public_key_pem.encode())

# 署名データを取得
signature_data = base64.b64decode(signature.split(":")[-1])

# 署名の検証
try:
    public_key.verify(
        signature_data,
        PAYLOAD.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("署名の検証に成功しました！")
except Exception as e:
    print("署名の検証に失敗しました:", str(e))
    exit(1)

