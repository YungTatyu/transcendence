#!/bin/bash

readonly SCRIPT_DIR=$(dirname $0)
readonly OUT_DIR="${SCRIPT_DIR}/${1:?error: missing argument}"
readonly CA_KEY="${SCRIPT_DIR}/ca.key"
readonly CA_CRT="${SCRIPT_DIR}/ca.crt"

readonly CLIENT_KEY="${SCRIPT_DIR}/client.key"
readonly CLIENT_CSR="${SCRIPT_DIR}/client.csr"
readonly CLIENT_CRT="${SCRIPT_DIR}/client.crt"

readonly SERVER_KEY="${OUT_DIR}/server.key"
readonly SERVER_CSR="${OUT_DIR}/server.csr"
readonly SERVER_CRT="${OUT_DIR}/server.crt"

readonly CONFIG="${SCRIPT_DIR}/openssl.cnf"

readonly KEY_LENGTH="2048"
readonly VALIDITY_DAYS="365"

# 既存の環境変数が設定されている場合はそれを使用し、なければデフォルトの値を使用
readonly C="${C:-JP}"
readonly ST="${ST:-Tokyo}"
readonly L="${L:-Shinjuku}"
readonly O="${O:-42tokyo}"
readonly OU="${OU:-IT}"
readonly CN="${1:?error: missing argument}"
readonly SUBJ="/C=${C}/ST=${ST}/L=${L}/O=${O}/OU=${OU}/CN=${CN}"
readonly SAN_DNS="${1:?error: missing argument}"
readonly SAN_IP="${SAN_IP:-0.0.0.0}"

# 証明書作成のために作られる一時ファイル
readonly TMP_CONFIG="tmp_openssl.cnf"

# 鍵と証明書がすでに存在するかチェック
check_files_exist() {
  if [[ -f "${ca_key}" && -f "${ca_crt}" && -f "${client_key}" && -f "${client_crt}" && -f "${server_key}" && -f "${server_crt}" ]]; then
    return 0
  fi
  return 1
}

add_read_permission() {
  for file in "$@"; do
    chmod +r "$file" || print_and_exit "failed to give permission to ${file}"
  done
  return 0
}

# 秘密鍵を生成
generate_keys() {
  echo "Generating keys..."
  if [[ ! -f "${CA_KEY}" ]]; then
    openssl genrsa -out "${CA_KEY}" "${KEY_LENGTH}" || return 1
  fi
  if [[ ! -f "${CLIENT_KEY}" ]]; then
    openssl genrsa -out "${CLIENT_KEY}" "${KEY_LENGTH}" || return 1
  fi
  openssl genrsa -out "${SERVER_KEY}" "${KEY_LENGTH}" || return 1
  add_read_permission ${CA_KEY} ${CLIENT_KEY} ${SERVER_KEY}
}

# 証明書署名要求 (CSR) を生成
generate_csr() {
  echo "Generating CSR for client and server..."
  if [[ ! -f "${CLIENT_CSR}" ]]; then
    openssl req -new -key "${CLIENT_KEY}" -out "${CLIENT_CSR}" -config "${CONFIG}" -sha256 -subj "${SUBJ}" || return 1
  fi
  openssl req -new -key "${SERVER_KEY}" -out "${SERVER_CSR}" -config "${CONFIG}" -sha256 -subj "${SUBJ}" || return 1
  add_read_permission ${CLIENT_CSR} ${SERVER_CSR}
}

# 証明書を生成
generate_certificates() {
  echo "Generating certificates..."
  cp "$CONFIG" "$TMP_CONFIG"
  echo >>${TMP_CONFIG}
  echo "[ alt_names ]" >>${TMP_CONFIG}
  echo "DNS = ${SAN_DNS}" >>${TMP_CONFIG}
  echo "IP  = ${SAN_IP}" >>${TMP_CONFIG}

  # トラップを設定して、TMP_CONFIGを削除
  trap 'rm -f ${TMP_CONFIG}' EXIT

  if [[ ! -f "${CA_CRT}" ]]; then
    openssl req -new -x509 -days "${VALIDITY_DAYS}" -key "${CA_KEY}" -out "${CA_CRT}" -config "${TMP_CONFIG}" -extensions v3_ca -sha256 -subj "${SUBJ}" || return 1
  fi
  if [[ ! -f "${CLIENT_CRT}" ]]; then
    openssl x509 -req -days "${VALIDITY_DAYS}" -in "${CLIENT_CSR}" -CA "${CA_CRT}" -CAkey "${CA_KEY}" -CAcreateserial -out "${CLIENT_CRT}" -extfile "${TMP_CONFIG}" -extensions v3_client -sha256 || return 1
  fi
  openssl x509 -req -days "${VALIDITY_DAYS}" -in "${SERVER_CSR}" -CA "${CA_CRT}" -CAkey "${CA_KEY}" -CAcreateserial -out "${SERVER_CRT}" -extfile "${TMP_CONFIG}" -extensions v3_server -sha256 || return 1
  add_read_permission ${CA_CRT} ${CLIENT_CRT} ${SERVER_CRT}
}

print_and_exit() {
  local message=$1
  local exit_code=$2
  echo "$message" >&2
  exit $exit_code
}

make_service_dir() {
  mkdir -p "${OUT_DIR}"
}

main() {
  # check_files_exist && print_and_exit "Secret key and certificate already exist." 0
  make_service_dir
  generate_keys || print_and_exit "failed to generate key" 1
  generate_csr || print_and_exit "failed to generate csr" 1
  generate_certificates || print_and_exit "failed to generate crt" 1
  echo "Certificate generation completed."
  return 0
}

main
