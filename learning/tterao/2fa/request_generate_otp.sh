#! /bin/bash

main() {
  local username=${1:?err}
  local password=${2:?err}
  local email=${3:?err}

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"${username}\",
      \"password\": \"${password}\",
      \"email\": \"${email}\"
    }" \
    http://localhost:8000/auth/otp/generate/

}

main "$@"
