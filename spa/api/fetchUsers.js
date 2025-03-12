export default async function fetchUsers(username = null, userId = null) {
  const authApiBaseUrl = "http://localhost:9000";
  const endpoint = "/users";

  if (
    (username === null && userId === null) ||
    (username !== null && userId !== null)
  ) {
    console.log("Please confirm fetchUsers function");
    return { status: null, data: null };
  }
  if (username !== null) {
    requestBody = { username: username };
  } else {
    requestBody = { userid: userId };
  }

  try {
    const response = await fetch(`${authApiBaseUrl}${endpoint}`, {
      method: "POST",
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
