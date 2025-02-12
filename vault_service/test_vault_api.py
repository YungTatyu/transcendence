import requests

VAULT_ADDR = "https://localhost:8200"

# クライアント証明書・秘密鍵・CA証明書のパス
CLIENT_CERT = "./create_cert/client.crt"
CLIENT_KEY = "./create_cert/client.key"
CA_CERT = "./create_cert/ca.crt"  # VaultのCA証明書（必要に応じて）

# Vaultの証明書認証エンドポイント
CERT_AUTH_URL = f"{VAULT_ADDR}/v1/auth/cert/login"

try:
    # クライアント証明書を使ってVaultにログイン
    response = requests.post(
        CERT_AUTH_URL, cert=(CLIENT_CERT, CLIENT_KEY), verify=CA_CERT
    )

    # レスポンスの処理
    if response.status_code == 200:
        token = response.json().get("auth", {}).get("client_token")
        print(f"Vaultログイン成功: トークン={token}")
    else:
        print(f"Vaultログイン失敗: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"リクエストエラー: {e}")
