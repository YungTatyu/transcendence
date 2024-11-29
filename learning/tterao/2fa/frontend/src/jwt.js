import { ACCESS_TOKEN_EXPIRES, BACKEND_BASE_URL } from "./constants.js";

export function decodeJwt(token) {
  const payload = token.split('.')[1];
  return JSON.parse(atob(payload));
}

async function refreshAccessToken(token) {
  const response = await fetch(`${BACKEND_BASE_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh: token })
  })
  const json = await response.json()
  console.log("refreshed token", json)
  if (!response.ok) {
    alert(json.error)
    return false
  }
  localStorage.setItem("authtoken", JSON.stringify(json))
  return true
}

export async function scheduleTokenRefresh(token) {
  const re = await refreshAccessToken(token);
  if (!re) {
    return false
  }
  setTimeout(async () => {
    console.log("refreshing token")
    scheduleTokenRefresh(token); // 次の更新をスケジュール ちょっと早めにスケジュールする
  }, ACCESS_TOKEN_EXPIRES * 60 * 1000 - (30 * 1000)); // 5分 (5分 × 60秒 × 1000ミリ秒)
  console.log("token refreshed")
  return true
}
