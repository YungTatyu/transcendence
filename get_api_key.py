import requests

# Vaultの設定
VAULT_HOST = "http://127.0.0.1:8200"
VAULT_TOKEN = "root"
SECRET_PATH = "transit/keys/api-key"
URL = f"{VAULT_HOST}/v1/{SECRET_PATH}"

# ヘッダーにVaultのトークンをセット
headers = {"X-Vault-Token": VAULT_TOKEN}
response = requests.post(URL, headers=headers)

# レスポンスのステータスコードを確認
if response.status_code != 200:
    print(f"Vaultからのデータ取得に失敗しました: {response.status_code}")
    print(response.text)
    exit(1)
else:
    data = response.json()
    print(data["data"]["keys"])
