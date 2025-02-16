# transitエンジンの署名エンドポイントを許可
path "transit/sign/jwt-key" {
  capabilities = ["create", "update"]
}

# 公開鍵リスト配信の取得許可
path "transit/keys/jwt-key" {
  capabilities = ["read"]
}
