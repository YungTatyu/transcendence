#!/bin/bash

CA_KEY="ca.key"
CA_CRT="ca.crt"
CA_CONFIG="ca_openssl.cnf"

SERVER_KEY="server.key"
SERVER_CSR="server.csr"
SERVER_CRT="server.crt"
SERVER_CONFIG="server_openssl.cnf"

KEY_LENGTH="2048"
VALIDITY_DAYS="365"

# 秘密鍵の作成
openssl genrsa -out ${CA_KEY} ${KEY_LENGTH}
openssl genrsa -out ${SERVER_KEY} ${KEY_LENGTH}

# 証明書署名要求の作成
openssl req -new -key ${SERVER_KEY} -out ${SERVER_CSR} -config ${SERVER_CONFIG}

# 証明書の作成
openssl req -new -x509 -days ${VALIDITY_DAYS} -key ${CA_KEY} -out ${CA_CRT} -config ${CA_CONFIG}
openssl x509 -req -days ${VALIDITY_DAYS} -in ${SERVER_CSR} -CA ${CA_CRT} -CAkey ${CA_KEY} -CAcreateserial -out ${SERVER_CRT} -extfile ${SERVER_CONFIG} -extensions req_ext
