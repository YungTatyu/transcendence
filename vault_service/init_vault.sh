#!/bin/sh

# Vaultサーバ起動
vault server -config=/vault/config/vault.hcl &

# Vaultサーバの起動待機
until vault status -tls-skip-verify 2>&1 | grep -q "Initialized"; do
  echo "Vault起動待機中..."
  sleep 2
done

# Vaultの初期化
init_output=$(vault operator init -tls-skip-verify -key-shares=1 -key-threshold=1 -format=json)
unseal_key=$(echo "$init_output" | sed -n '/"unseal_keys_b64": \[/,/]/p' | grep -o '.*="$' | sed 's/\s*"//g')
root_token=$(echo "$init_output" | grep -o '"root_token": "[^"]*"' | sed 's/"root_token": "//' | sed 's/"//g')

# Vaultアンシール
vault operator unseal -tls-skip-verify $unseal_key
# Vault設定: transitシークレットエンジンの有効化と署名キー作成
export VAULT_TOKEN=$root_token
vault secrets enable -tls-skip-verify transit
vault write -tls-skip-verify -f transit/keys/signing-key type=rsa-2048

# TLS認証の設定
vault auth enable -tls-skip-verify cert
vault write -tls-skip-verify auth/cert/certs/client \
    display_name="client" \
    policies="default" \
    certificate="$(cat /vault/certs/client.crt)"

echo "Vault ルートトークン: $root_token"
tail -f /dev/null
