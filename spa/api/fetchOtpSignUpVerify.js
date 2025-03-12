import config from "../../config.js";

export default async function fetchOtpSignUpVerify(username, otp) {
  const authApiBaseUrl = config.authService;
  const endpoint = "/auth/otp/signup/verify";

  const requestBody = { username: username, otp: otp };

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
