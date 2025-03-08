import Footer from "../components/Footer.js";
import Header from "../components/Header.js";
import stateManager from "../stateManager.js";

export default function SignUp() {
  return `
    ${Header({ title: "signup" })}
    <img id="qrCode" alt="QR Code">
    <label for="otp">OTP:</label>
    <input type="number" id="otp" name="otp" required><br><br>
    <button id="signUpVerifyButton">verify</button>
    ${Footer({ text: "© 2025 My Company" })}
  `;
}

export function setupSignUpVerify() {
  const signUpVerifyButton = document.getElementById("signUpVerifyButton");

  const qrCode = stateManager.state.qr;
  const imgElement = document.getElementById("qrCode");
  imgElement.src = qrCode;

  signUpVerifyButton.addEventListener("click", async () => {
    const resData = await fetchOtpSignUpVerify();
    if (resData == null) {
      return;
    }
    console.log(resData);
  });
}

async function fetchOtpSignUpVerify() {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/signup/verify";

  const requestBody = {
    username: stateManager.state.username,
    otp_token: document.getElementById("otp").value,
  };

  try {
    const response = await fetch(`${authApiBaseUrl}${endpoint}`, {
      method: "POST",
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
