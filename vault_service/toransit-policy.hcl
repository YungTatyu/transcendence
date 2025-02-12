# transitエンジンの署名エンドポイントを許可
path "transit/sign/jwt-key" {
  capabilities = ["create", "update"]
}

# キーリストの取得許可（オプション）
path "transit/keys/jwt-key" {
  capabilities = ["read"]
}
