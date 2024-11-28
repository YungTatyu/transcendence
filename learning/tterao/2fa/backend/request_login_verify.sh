#! /bin/bash

main() {
  local username=${1:?err}
  local otp=${2:?err}

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
      \"otp\": \"${otp}\",
      \"username\": \"${username}\"
    }" \
    http://localhost:8000/auth/login/otp/verify/

}

main "$@"
