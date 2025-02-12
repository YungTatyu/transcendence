storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/vault/certs/vault.crt"  # VaultサーバーのTLS証明書
  tls_key_file  = "/vault/certs/vault.key"  # VaultサーバーのTLS秘密鍵
  tls_client_ca_file = "/vault/certs/ca.crt"
  tls_disable = "false"
}

disable_mlock = true
