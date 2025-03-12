import config from "../../config.js";

export default async function fetchUpdateUserName(username) {
  const userApiBaseUrl = config.userService;
  const endpoint = "/users/me/username";

  const requestBody = { username: username };

  try {
    const response = await fetch(`${userApiBaseUrl}${endpoint}`, {
      method: "PUT",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    const status = response.status;
    const data = await response.json();
    return { status: status, data: data };
  } catch (error) {
    console.error("API fetch error: ", error);
    return { status: null, data: null };
  }
}
