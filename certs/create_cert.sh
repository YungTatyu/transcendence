#!/bin/bash

SCRIPT_DIR=$(dirname $0)
CA_KEY="${SCRIPT_DIR}/ca.key"
CA_CRT="${SCRIPT_DIR}/ca.crt"
CA_CSR="${SCRIPT_DIR}/ca.csr"
CA_CONFIG="${SCRIPT_DIR}/ca_openssl.cnf"

CLIENT_KEY="${SCRIPT_DIR}/client.key"
CLIENT_CSR="${SCRIPT_DIR}/client.csr"
CLIENT_CRT="${SCRIPT_DIR}/client.crt"
CLIENT_CONFIG="${SCRIPT_DIR}/client_openssl.cnf"

SERVER_KEY="${SCRIPT_DIR}/server.key"
SERVER_CSR="${SCRIPT_DIR}/server.csr"
SERVER_CRT="${SCRIPT_DIR}/server.crt"
SERVER_CONFIG="${SCRIPT_DIR}/server_openssl.cnf"

KEY_LENGTH="2048"
VALIDITY_DAYS="365"

# 鍵と証明書がある場合はスクリプトを終了
if [[ -f "${CA_KEY}" && -f "${CA_CRT}" && -f "${CLIENT_KEY}" && -f "${CLIENT_CRT}" && -f "${SERVER_KEY}" && -f "${SERVER_CRT}" ]]; then
	echo "secret key and certificate already exist."
	exit 0
fi

# 秘密鍵の作成
openssl genrsa -out ${CA_KEY} ${KEY_LENGTH}
openssl genrsa -out ${CLIENT_KEY} ${KEY_LENGTH}
openssl genrsa -out ${SERVER_KEY} ${KEY_LENGTH}

# 証明書署名要求の作成
openssl req -new -key ${CLIENT_KEY} -out ${CLIENT_CSR} -config ${CLIENT_CONFIG} -sha256
openssl req -new -key ${SERVER_KEY} -out ${SERVER_CSR} -config ${SERVER_CONFIG} -sha256

# 証明書の作成
openssl req -new -x509 -days ${VALIDITY_DAYS} -key ${CA_KEY} -out ${CA_CRT} -config ${CA_CONFIG} -extensions v3_ca -sha256
openssl x509 -req -days ${VALIDITY_DAYS} -in ${CLIENT_CSR} -CA ${CA_CRT} -CAkey ${CA_KEY} -CAcreateserial -out ${CLIENT_CRT} -extfile ${CLIENT_CONFIG} -extensions req_ext -sha256
openssl x509 -req -days ${VALIDITY_DAYS} -in ${SERVER_CSR} -CA ${CA_CRT} -CAkey ${CA_KEY} -CAcreateserial -out ${SERVER_CRT} -extfile ${SERVER_CONFIG} -extensions req_ext -sha256
