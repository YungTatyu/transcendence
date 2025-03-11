export default async function fetchOtpSignUp(username, password, email) {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/signup";

  const requestBody = { username: username, email: email, password: password };

  try {
    const response = await fetch(`${authApiBaseUrl}${endpoint}`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error! Status: ${response.status}`);
    }

    const resData = await response.json();
    return resData.qr_code;
  } catch (error) {
    console.error("API fetch error: ", error);
    return null;
  }
}
