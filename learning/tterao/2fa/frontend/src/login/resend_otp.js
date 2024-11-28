import { BACKEND_BASE_URL } from '../constants.js'
export async function resendOtp(event) {
  event.preventDefault()

  const response = await fetch(`${BACKEND_BASE_URL}/auth/login/otp/resend/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: localStorage.getItem("username") })
  })
  const json = await response.json()
  console.log(json)
  if (!response.ok) {
    alert(json.error || "request failed.")
    return false
  }
  return true
}
