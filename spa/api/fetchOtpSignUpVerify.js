export default async function fetchOtpSignUpVerify(username, otp) {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/signup/verify";

  const requestBody = { username: username, otp: otp };

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
    return resData;
  } catch (error) {
    console.error("API fetch error: ", error);
    return null;
  }
}
