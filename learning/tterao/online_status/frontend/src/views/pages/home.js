import { ACCESS_TOKEN, BACKEND_BASE_URL, REFRESH_TOKEN } from "../../config/constants.js"

export async function logoutEvent(event) {
  event.preventDefault()
  const accessToken = localStorage.getItem(ACCESS_TOKEN)
  const refreshToken = localStorage.getItem(REFRESH_TOKEN)
  const response = await fetch(`${BACKEND_BASE_URL}/api/logout/`, {
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
  localStorage.removeItem(ACCESS_TOKEN)
  localStorage.removeItem(REFRESH_TOKEN)
  window.location.pathname = '/';
  return true
}

function wsUserStatus() {
  const socket = new WebSocket('ws://localhost:8000/status/')

  socket.onmessage = function(event) {
    console.log('Received message:', event.data);
    const data = JSON.parse(event.data);
    if (data.type === 'all_statuses') {
      const statuses = data.statuses;
      const statusList = document.querySelector(".js-user-status")
      statusList.innerHTML = ''; // リストをリセット
      Object.entries(statuses).forEach(([user, status]) => {
        if (status !== 'active') {
          return
        }
        const listItem = document.createElement('li');
        listItem.textContent = `${user}: online`;
        listItem.style.color = 'green'; // オンラインを緑色で表示
        statusList.appendChild(listItem);
      });
    }
  };

  socket.onerror = function(error) {
    console.error('WebSocket Error:', error);
  };

  socket.onclose = function(event) {
    console.log('WebSocket connection closed', event);
  };
}

export const home = {
  render: function() {
    return `
    <div class="container mt-5">
      <div class="d-flex justify-content-between align-items-center">
        <h2>Welcome</h2>
        <ul class="list-unstyled js-user-status"></ul>
      </div>
      <button type="submit" class="btn btn-primary logout mb-3">Logout</button>
      <div class="content">
        <p>Here is your homepage content!</p>
      </div>
    </div>
`
  },
  initializeEvents: async function() {
    document.querySelector(".logout").addEventListener("click", logoutEvent)
    wsUserStatus()
  }
}

