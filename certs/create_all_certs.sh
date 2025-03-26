#!/bin/bash

readonly SCRIPT_DIR=$(dirname $0)
readonly CREATE_CERT=${SCRIPT_DIR}/create_cert.sh

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

main() {
  services=(
    "auth_app"
    "game"
    "tournament"
    "user_app"
    "friends_activity_app"
    "friends"
    "match"
    "vault"
    "auth-proxy.transcen.com"
    "game_proxy_server"
    "tournament_proxy_server"
    "user_proxy_server"
    "friends_activity_proxy_server"
    "friends_proxy_server"
    "match_proxy_server"
    "www.transcen.com"
  )
  for service in "${services[@]}"; do
    ${CREATE_CERT} $service || err "$service cert creation failed"
  done
  return 0
}

main "$@"
