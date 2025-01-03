const apiBaseUrl = "http://localhost:8000/api";

// Register user
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch(`${apiBaseUrl}/register/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    document.getElementById('register-result').textContent = response.ok ? result.message : JSON.stringify(result);
});

// Login user
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch(`${apiBaseUrl}/login/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    document.getElementById('login-result').textContent = response.ok ? `Token: ${result.token}` : result.error;
});

// Send friend request
document.getElementById('friend-request-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const from_user = document.getElementById('from-user').value;
    const to_user = document.getElementById('to-user').value;

    const token = localStorage.getItem("authToken");

    const response = await fetch(`${apiBaseUrl}/friend-requests/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({ from_user, to_user })
    });

    const result = await response.json();
    document.getElementById('friend-request-result').textContent = response.ok ? result.message : JSON.stringify(result);
});
