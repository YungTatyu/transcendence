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

    if (!response.ok) {
      throw new Error(`HTTP Error! Status: ${response.status}`);
    }

    const resData = await response.json();
    return resData;
  } catch (error) {
    console.error("API fetch error: ", error);
    return null;
  }
}
