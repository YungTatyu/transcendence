#! /bin/bash

main() {
  local username=${1:?err}
  local otp=${2:?err}

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"${username}\",
      \"otp\": \"${otp}\"
    }" \
    http://localhost:8000/auth/otp/verify/

}

main "$@"
