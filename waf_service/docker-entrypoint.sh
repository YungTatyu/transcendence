#! /bin/bash

readonly DEFAULT_CONF='/etc/nginx/conf.d/default.conf'

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

envsubst <${DEFAULT_CONF} >${DEFAULT_CONF} || {
  err "failed to convert env vars"
  exit 1
}
exec "$@"
