import { BACKEND_BASE_URL } from "../constants.js";
import { showPage } from '../showpage.js'

export async function logout(event) {
  event.preventDefault()
  const accessToken = JSON.parse(localStorage.getItem("authtoken")).access
  const response = await fetch(`${BACKEND_BASE_URL}/auth/logout/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken,
    },
  })
  const json = await response.json()
  if (!response.ok) {
    alert(json.error || "logout failed.")
    return false
  }
  showPage("login")
  return true
}

export function addLoginEvent() {
  document.querySelector(".logout").addEventListener("submit", logout)
}
