# transitエンジンの署名エンドポイントを許可
path "transit/sign/jwt-key" {
  capabilities = ["create", "update"]
}

# 公開鍵リスト配信の取得許可
path "transit/keys/jwt-key" {
  capabilities = ["read"]
}

# UsersAPI用APIキーの取得を許可
path "transit/keys/api-key-users" {
  capabilities = ["read"]
}

# Matches用APIキーの取得を許可
path "transit/keys/api-key-matches" {
  capabilities = ["read"]
}

# Tournaments用APIキーの取得を許可
path "transit/keys/api-key-tournaments" {
  capabilities = ["read"]
}
