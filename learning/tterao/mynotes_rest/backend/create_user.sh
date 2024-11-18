# ! /bin/bash

main() {
  local username="${1:?err}"
  local password="${2:?err}"
  curl -X POST http://127.0.0.1:8000/users/create/ \
    -H "Content-Type: application/json" \
    -d "{
    \"username\": \"$username\",
    \"password\": \"$password\"
  }" || {
    echo >&2 "err: api request failed"
    return 1
  }
  return 0

}

main "$@"
