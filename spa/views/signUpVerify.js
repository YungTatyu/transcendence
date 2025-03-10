import generateVerifyForm from "../components/verifyForm.js";
import stateManager from "../stateManager.js";

export default function SignUpVerify() {
  const formHtml = generateVerifyForm(
    true,
    "Scan this QRcode and verify OTP",
    6,
    "signUpVerifyButton",
  );
  return formHtml;
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

    const updateEmailButton = document.getElementById("updateEmail");
    updateEmailButton.addEventListener("click", async () => {
      const resData = await fetchUpdateEmail();
      if (resData == null) {
        return;
      }
      console.log(resData);
    });
  });
}

async function fetchOtpSignUpVerify() {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/signup/verify";

  const requestBody = {
    username: stateManager.state.username,
    otp: Array.from(document.querySelectorAll(".otp-input")),
  };

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

async function fetchUpdateEmail() {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/me/email";

  const requestBody = {
    email: document.getElementById("email").value,
  };

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
