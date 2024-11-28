import { BACKEND_BASE_URL } from "../constants.js";
import { showPage } from '../showpage.js'

export async function login(event) {
  event.preventDefault()
  const username = event.target.username.value
  const password = event.target.password.value
  const response = await fetch(`${BACKEND_BASE_URL}/auth/login/otp/generate/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: username, password: password })
  })
  const json = await response.json()
  console.log(json)
  if (!response.ok) {
    alert(json.error || "login failed.")
    return false
  }
  localStorage.setItem('username', username)
  showPage("otp")
  return true
}

export function addLoginEvent() {
  document.querySelector(".login-form").addEventListener("submit", login)
}
