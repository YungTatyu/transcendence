#! /bin/bash

main() {
  local username=${1:?err}

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"${username}\"
    }" \
    http://localhost:8000/auth/login/otp/resend/

}

main "$@"
