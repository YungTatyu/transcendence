import { BACKEND_BASE_URL } from "../constants.js";
import { showPage } from "../showpage.js";
import { resendOtp } from "./resend_otp.js";

export async function verifyOtp(event) {
  event.preventDefault()

  const otpInputs = Array.from(event.target.querySelectorAll('input[type="text"]'));
  const otp = otpInputs.reduce((acc, input) => acc + input.value, '');

  const response = await fetch(`${BACKEND_BASE_URL}/auth/login/otp/verify/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: localStorage.getItem("username"), otp: otp })
  })
  const json = await response.json()
  console.log(json)
  if (!response.ok) {
    alert(json.error || "request failed.")
    return false
  }
  localStorage.removeItem("username")
  localStorage.setItem("authtoken", JSON.stringify(json))
  showPage("home")
  return true
}

export function addVerifyOtpEvent() {
  document.querySelector(".otp-form").addEventListener("submit", verifyOtp)
  document.querySelector(".js-resend-otp").addEventListener("click", resendOtp)
}
