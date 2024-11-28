import { BACKEND_BASE_URL } from "../constants.js";
import { showPage } from '../showpage.js'

export async function signup(event) {
  event.preventDefault()
  const username = event.target.username.value
  const password = event.target.password.value
  const email = event.target.email.value
  const response = await fetch(`${BACKEND_BASE_URL}/auth/otp/generate/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: username, password: password, email: email })
  })
  const json = await response.json()
  console.log(json)
  if (!response.ok) {
    alert(json.error || "signup failed.")
    return false
  }
  localStorage.setItem('username', username)
  showPage("otp")
  return true
}

export function addSignupEvent() {
  document.querySelector(".signup-form").addEventListener("submit", signup)
  document.getElementById("go-to-login").addEventListener("click", () => showPage("login"))
}
