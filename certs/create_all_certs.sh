#!/bin/bash

readonly SCRIPT_DIR=$(dirname $0)
readonly CREATE_CERT=${SCRIPT_DIR}/create_cert.sh

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

main() {
  services=(
    "vault"
    "auth-proxy.transcen.com"
    "game-proxy.transcen.com"
    "tournament-proxy.transcen.com"
    "user-proxy.transcen.com"
    "friends-activity-proxy.transcen.com"
    "friends-proxy.transcen.com"
    "match-proxy.transcen.com"
    "www.transcen.com"
    "localhost" # INFO: localhostで動かす用
  )
  for service in "${services[@]}"; do
    ${CREATE_CERT} $service || err "$service cert creation failed"
  done
  return 0
}

main "$@"
