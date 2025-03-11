export default async function fetchUpdateEmail(email) {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/me/email";

  const requestBody = { email: email };

  try {
    const response = await fetch(`${authApiBaseUrl}${endpoint}`, {
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
