# Vaultサービス

## ファイル構成
```
.
|── certs
│   ├── create_cert.sh      # 秘密鍵等を生成するスクリプト
│   ├── *_openssl.cnf       # 秘密鍵等を生成する際に使用する設定ファイル
|
|── vault_service
    ├── Dockerfile
    ├── config
    │   ├── transit-policy.hcl  # 署名・公開鍵配信用のエンドポイントに適用するセキュリティポリシーを記述するconfigファイル
    │   └── vault.hcl           # Vaultの基本的な設定を記述するconfigファイル
    ├── init_vault.sh           # Vaultの初期化を行うためのスクリプト
    └── vault_client
        ├── jwt_utils.py        # JWTに関する汎用関数群を記述
        └── vault_client.py     # Vaultサーバのエンドポイントを叩く処理を記述
```

## 簡易実行方法
1. `make`を実行し、秘密鍵等を生成&Vaultサーバを立ち上げる
2. `cd vaulr_service/vault_client ; python3 vault_client.py`を実行すると、\
    [トークンの取得 -> 署名の作成 -> 検証用公開鍵の取得 -> 署名の検証] \
    が実行されます。

## APIサーバでの運用方法
1. docker-compose.ymlファイルのサービスのVolume設定を追加し、certsファイルをDockerfile内で使用できるようにする。
```
    volumes:
        - ./certs/client.crt:/path/to/certs/client.crt:ro
        - ./certs/client.key:/path/to/certs/client.key:ro
        - ./certs/ca.crt:/path/to/certs/ca.crt:ro
```
2. `vault_client.py`のような処理でVaultサーバのAPIを叩く(vault_client.pyを用いる場合、VAULT_ADDRのホスト名を適切に変更してください)
