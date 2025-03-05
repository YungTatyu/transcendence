#!/bin/bash

# Vaultサーバの起動待機
until vault status 2>&1 | grep -q "Initialized"; do
	echo "Vault起動待機中..."
	sleep 2
done

# Vaultの初期化
init_output=$(vault operator init -key-shares=1 -key-threshold=1 -format=json)
unseal_key=$(echo "$init_output" | sed -n '/"unseal_keys_b64": \[/,/]/p' | grep -o '.*="$' | sed 's/\s*"//g')
root_token=$(echo "$init_output" | grep -o '"root_token": "[^"]*"' | sed 's/"root_token": "//' | sed 's/"//g')

# Vaultアンシール
vault operator unseal $unseal_key
# Vault設定: transitシークレットエンジンの有効化と署名キー作成
export VAULT_TOKEN=$root_token
vault secrets enable transit
vault write -f transit/keys/jwt-key type=rsa-2048
vault read transit/keys/jwt-key

# APIキー配信用の設定
AUTO_ROTATE_PERIOD="auto_rotate_period=24h"
vault write transit/keys/api-key-users ${AUTO_ROTATE_PERIOD}
vault write transit/keys/api-key-matches ${AUTO_ROTATE_PERIOD}
vault write transit/keys/api-key-tournaments ${AUTO_ROTATE_PERIOD}

# ポリシーを作成
vault policy write transit-policy /vault/config/transit-policy.hcl

# TLS認証の設定
vault auth enable cert
vault write auth/cert/certs/client \
	display_name="client" \
	policies="default,transit-policy" \
	certificate="$(cat /vault/certs/ca.crt)"

echo "Vault ルートトークン: $root_token"
