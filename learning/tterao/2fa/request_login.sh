#! /bin/bash

main() {
  local username=${1:?err}
  local password=${2:?err}

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"${username}\",
      \"password\": \"${password}\"
    }" \
    http://localhost:8000/auth/login/otp/generate/

}

main "$@"
