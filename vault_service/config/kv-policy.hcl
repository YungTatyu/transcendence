# APIキーの取得を許可
path "kv/apikeys/*" {
  capabilities = ["read"]
}
