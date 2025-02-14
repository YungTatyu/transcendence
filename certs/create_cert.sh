#!/bin/bash

SCRIPT_DIR=$(dirname $0)
CA_KEY="${SCRIPT_DIR}/ca.key"
CA_CRT="${SCRIPT_DIR}/ca.crt"

CLIENT_KEY="${SCRIPT_DIR}/client.key"
CLIENT_CSR="${SCRIPT_DIR}/client.csr"
CLIENT_CRT="${SCRIPT_DIR}/client.crt"

SERVER_KEY="${SCRIPT_DIR}/server.key"
SERVER_CSR="${SCRIPT_DIR}/server.csr"
SERVER_CRT="${SCRIPT_DIR}/server.crt"

CONFIG="${SCRIPT_DIR}/openssl.cnf"

KEY_LENGTH="2048"
VALIDITY_DAYS="365"

# 既存の環境変数が設定されている場合はそれを使用し、なければデフォルトの値を使用
C="${C:-JP}"
ST="${ST:-Tokyo}"
L="${L:-Shinjuku}"
O="${O:-42tokyo}"
OU="${OU:-IT}"
CN="${CN:-localhost}"
SUBJ="/C=${C}/ST=${ST}/L=${L}/O=${O}/OU=${OU}/CN=${CN}"

# 鍵と証明書がすでに存在するかチェック
check_files_exist() {
    if [[ -f "${CA_KEY}" && -f "${CA_CRT}" && -f "${CLIENT_KEY}" && -f "${CLIENT_CRT}" && -f "${SERVER_KEY}" && -f "${SERVER_CRT}" ]]; then
        echo "Secret key and certificate already exist."
        exit 0
    fi
}

# 秘密鍵を生成
generate_keys() {
    echo "Generating keys..."
    openssl genrsa -out "${CA_KEY}" "${KEY_LENGTH}"
    openssl genrsa -out "${CLIENT_KEY}" "${KEY_LENGTH}"
    openssl genrsa -out "${SERVER_KEY}" "${KEY_LENGTH}"
}

# 証明書署名要求 (CSR) を生成
generate_csr() {
    echo "Generating CSR for client and server..."
    openssl req -new -key "${CLIENT_KEY}" -out "${CLIENT_CSR}" -config "${CONFIG}" -sha256 -subj "${SUBJ}"
    openssl req -new -key "${SERVER_KEY}" -out "${SERVER_CSR}" -config "${CONFIG}" -sha256 -subj "${SUBJ}"
}

# 証明書を生成
generate_certificates() {
    echo "Generating certificates..."
    openssl req -new -x509 -days "${VALIDITY_DAYS}" -key "${CA_KEY}" -out "${CA_CRT}" -config "${CONFIG}" -extensions v3_ca -sha256 -subj "${SUBJ}"
    openssl x509 -req -days "${VALIDITY_DAYS}" -in "${CLIENT_CSR}" -CA "${CA_CRT}" -CAkey "${CA_KEY}" -CAcreateserial -out "${CLIENT_CRT}" -extfile "${CONFIG}" -extensions v3_client -sha256
    openssl x509 -req -days "${VALIDITY_DAYS}" -in "${SERVER_CSR}" -CA "${CA_CRT}" -CAkey "${CA_KEY}" -CAcreateserial -out "${SERVER_CRT}" -extfile "${CONFIG}" -extensions v3_server -sha256
}

# メイン処理
main() {
    check_files_exist
    generate_keys
    generate_csr
    generate_certificates
    echo "Certificate generation completed."
}

main
