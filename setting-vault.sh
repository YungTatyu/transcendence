#!/bin/bash

# JWTへの署名＆公開鍵の配信エンドポイント作成
vault secrets enable transit
vault write -f transit/keys/signing-key type=rsa-2048
vault read transit/keys/signing-key
## policy.hclをvaultコンテナ内に下記の内容で作成する
"""
path "transit/keys/signing-key" {
  capabilities = ["read"]
}
"""
vault policy write public-key-policy policy.hcl
vault token create -policy=public-key-policy


# 環境変数配信エンドポイント作成
vault secrets enable -path=env-vars kv
## users.secret.jsonをvaultコンテナ内に下記の内容で作成する
"""
{
"MASTER_ID":"0",
"FLAG": "true"
}
"""
vault kv put env-vars/users @/users.secret.json

