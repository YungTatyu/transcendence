#!/bin/bash

CA_KEY="ca.key"
CA_CRT="ca.crt"
CA_CSR="ca.csr"
CA_CONFIG="ca_openssl.cnf"

CLIENT_KEY="client.key"
CLIENT_CSR="client.csr"
CLIENT_CRT="client.crt"
CLIENT_CONFIG="client_openssl.cnf"

VAULT_KEY="vault.key"
VAULT_CSR="vault.csr"
VAULT_CRT="vault.crt"
VAULT_CONFIG="vault_openssl.cnf"

KEY_LENGTH="2048"
VALIDITY_DAYS="365"

# 秘密鍵の作成
openssl genrsa -out ${CA_KEY} ${KEY_LENGTH}
openssl genrsa -out ${CLIENT_KEY} ${KEY_LENGTH}
openssl genrsa -out ${VAULT_KEY} ${KEY_LENGTH}



# 証明書署名要求の作成
openssl req -new -key ${CLIENT_KEY} -out ${CLIENT_CSR} -config ${CLIENT_CONFIG} -sha256
openssl req -new -key ${VAULT_KEY} -out ${VAULT_CSR} -config ${VAULT_CONFIG} -sha256

# 証明書の作成
openssl req -new -x509 -days ${VALIDITY_DAYS} -key ${CA_KEY} -out ${CA_CRT} -config ${CA_CONFIG} -extensions v3_ca -sha256
openssl x509 -req -days ${VALIDITY_DAYS} -in ${CLIENT_CSR} -CA ${CA_CRT} -CAkey ${CA_KEY} -CAcreateserial -out ${CLIENT_CRT} -extfile ${CLIENT_CONFIG} -extensions req_ext -sha256
openssl x509 -req -days ${VALIDITY_DAYS} -in ${VAULT_CSR} -CA ${CA_CRT} -CAkey ${CA_KEY} -CAcreateserial -out ${VAULT_CRT} -extfile ${VAULT_CONFIG} -extensions req_ext -sha256
