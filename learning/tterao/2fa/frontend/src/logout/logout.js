import { BACKEND_BASE_URL } from "../constants.js";
import { showPage } from '../showpage.js'

export async function logout(event) {
  event.preventDefault()
  const authToken = JSON.parse(localStorage.getItem("authtoken"))
  const accessToken = authToken.access
  const refreshToken = authToken.refresh
  const response = await fetch(`${BACKEND_BASE_URL}/auth/logout/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken,
    },
    body: JSON.stringify({ refresh: refreshToken })
  })
  const json = await response.json()
  if (!response.ok) {
    alert(json.error || "logout failed.")
    return false
  }
  showPage("login")
  return true
}

export function addLogoutEvent() {
  document.querySelector(".logout").addEventListener("click", logout)
}
