import { ACCESS_TOKEN, BACKEND_BASE_URL, REFRESH_TOKEN } from "../../config/constants.js";

export async function loginEvent(event) {
  event.preventDefault()
  const username = event.target.username.value
  const password = event.target.password.value
  const response = await fetch(`${BACKEND_BASE_URL}/api/token/`, {
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
  localStorage.setItem(ACCESS_TOKEN, json.access)
  localStorage.setItem(REFRESH_TOKEN, json.refresh)
  window.location.pathname = '/';
  return true
}

export const login = {
  render: function() {
    return `
      <div id = "login-page" class="container mt-5 d-flex justify-content-center align-items-center text-center" >
        <div class="position-relative">
          <h2 class="mb-3">Login</h2>
          <form class="login-form">
            <div class="mb-3">
              <input type="text" class="form-control" name="username" placeholder="Username" required />
            </div>
            <div class="mb-3"> <input type="password" class="form-control" name="password" placeholder="Password"
              required />
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
          </form>
        </div>
    </div >
  `
  },
  initializeEvents: async function() {
    document.querySelector(".login-form").addEventListener("submit", loginEvent)
  }
}
