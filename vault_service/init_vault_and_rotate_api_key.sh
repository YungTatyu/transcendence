#!/bin/bash

print_log_and_exit() {
	local message=$1
	local exit_code=${2:-1} # デフォルト値を1に設定
	echo "[$(date '+%Y-%m-%dT%H:%M:%S%z')]: $message" >&2
	exit $exit_code
}

# Vaultサーバの起動待機
wait_for_vault() {
	local timeout=60
	local elapsed=0

	until vault status 2>&1 | grep -q "Initialized"; do
		echo "Vault起動待機中..."
		sleep 2
		((elapsed += 2))

		if [ "$elapsed" -ge "$timeout" ]; then
			print_log_and_exit "Vaultの起動を60秒待ちましたが、応答がありません。"
		fi
	done
}

initialize_vault() {
	readonly VAULT_UNSEAL_KEY_FILE="${VAULT_UNSEAL_KEY_FILE:-/vault/keys/unseal_key}"
	readonly VAULT_ROOT_TOKEN_FILE="${VAULT_ROOT_TOKEN_FILE:-/vault/keys/root_token}"

	# すでに保存されたキーが存在するか？
	if [[ -f "$VAULT_UNSEAL_KEY_FILE" && -f "$VAULT_ROOT_TOKEN_FILE" ]]; then
		echo "既存のunseal keyおよびroot tokenを使用します"
		local unseal_key
		local root_token

		unseal_key=$(<"$VAULT_UNSEAL_KEY_FILE")
		root_token=$(<"$VAULT_ROOT_TOKEN_FILE")
		export VAULT_TOKEN=$root_token
	else
		echo "Vaultを初期化します"
		local init_output
		local unseal_key
		local root_token

		init_output=$(vault operator init -key-shares=1 -key-threshold=1 -format=json)

		unseal_key=$(echo "$init_output" | jq -r '.unseal_keys_b64[0]')
		root_token=$(echo "$init_output" | jq -r '.root_token')
		export VAULT_TOKEN=$root_token

		# キーを保存
		echo "$unseal_key" > "$VAULT_UNSEAL_KEY_FILE"
		echo "$root_token" > "$VAULT_ROOT_TOKEN_FILE"
		chmod 600 "$VAULT_UNSEAL_KEY_FILE" "$VAULT_ROOT_TOKEN_FILE"
	fi

	# Vaultアンシール
	if ! vault operator unseal "$unseal_key"; then
		print_log_and_exit "Vaultアンシールに失敗しました"
	fi
}


# Vault設定: transitシークレットエンジンの有効化と署名キー作成
enable_transit() {
	if ! vault secrets enable transit; then
		print_log_and_exit "transitシークレットエンジンの有効化に失敗しました"
	fi
	if ! vault write -f transit/keys/jwt-key type=rsa-2048; then
		print_log_and_exit "署名キーの作成に失敗しました"
	fi
	if ! vault read transit/keys/jwt-key; then
		print_log_and_exit "JWTキーの読み取りに失敗しました"
	fi
}

# APIキー配信用の設定
enable_api_keys() {
	if ! vault secrets enable -path=kv/apikeys -description="kv for APIKey" kv; then
		print_log_and_exit "APIキーのkv設定に失敗しました"
	fi
}

# TLS認証の設定
enable_tls_auth() {
	# ポリシーを作成
	if ! vault policy write transit-policy /vault/config/transit-policy.hcl; then
		print_log_and_exit "transit-policy の適用に失敗しました"
	fi

	if ! vault policy write kv-policy /vault/config/kv-policy.hcl; then
		print_log_and_exit "kv-policy の適用に失敗しました"
	fi

	if ! vault auth enable cert; then
		print_log_and_exit "TLS認証の設定に失敗しました"
	fi

	if ! vault write auth/cert/certs/client \
		display_name="client" \
		policies="default,transit-policy,kv-policy" \
		certificate="$(cat /vault/certs/ca.crt)"; then
		print_log_and_exit "TLS証明書の設定に失敗しました"
	fi
}

gen_api_key() {
	echo $(openssl rand -base64 12 | tr -dc 'A-Za-z0-9')
}

# APIキーを更新する関数
update_api_key() {
	local key_name=$1
	local old_key=$2
	local new_key=$3

	# APIキー更新の前に引数チェック
	if [ -z "$key_name" ] || [ -z "$old_key" ] || [ -z "$new_key" ]; then
		print_log_and_exit "無効な引数が渡されました"
	fi

	# 新しいAPIキーを保存し、前のAPIキーを previous_value に保存
	if ! vault kv put kv/apikeys/$key_name value="$new_key" previous_value="$old_key"; then
		print_log_and_exit "APIキー '$key_name' の更新に失敗しました。"
	fi
}

update_api_keys_loop() {
	readonly API_KEY_ROTATE_SEC=${API_KEY_ROTATE_SEC:-3600}

	local current_users_key=$(gen_api_key)
	local current_matches_key=$(gen_api_key)
	local current_tournaments_key=$(gen_api_key)
	local current_games_key=$(gen_api_key)

	# 🔁 APIキーを更新
	while true; do
		# 新しいランダムなAPIキーを生成
		local new_users_key=$(gen_api_key)
		local new_matches_key=$(gen_api_key)
		local new_tournaments_key=$(gen_api_key)
		local new_games_key=$(gen_api_key)

		# 新しいAPIキーを保存し、前のAPIキーを previous_value に保存
		update_api_key "users" "$current_users_key" "$new_users_key"
		update_api_key "matches" "$current_matches_key" "$new_matches_key"
		update_api_key "tournaments" "$current_tournaments_key" "$new_tournaments_key"
		update_api_key "games" "$current_games_key" "$new_games_key"

		current_users_key=$new_users_key
		current_matches_key=$new_matches_key
		current_tournaments_key=$new_tournaments_key
		current_games_key=$new_games_key

		sleep ${API_KEY_ROTATE_SEC}
	done
}

main() {
	wait_for_vault
	initialize_vault
	enable_transit
	enable_api_keys
	enable_tls_auth
	update_api_keys_loop
}

main
