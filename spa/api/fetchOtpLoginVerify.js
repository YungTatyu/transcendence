export default async function fetchOtpSignUpVerify(email, otp) {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/login/verify";

  const requestBody = { email: email, otp: otp };

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
