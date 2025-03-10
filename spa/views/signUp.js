import stateManager from "../stateManager.js";
import generateForm from "../components/form.js";

export default function SignUp() {
  const signUpFormFields = [
    { label: "Username", type: "text", placeholder: "User", required: true },
    {
      label: "Password",
      type: "password",
      placeholder: "password123",
      required: true,
    },
    {
      label: "Mail",
      type: "email",
      placeholder: "sample@example.com",
      required: true,
    },
  ];
  return generateForm(signUpFormFields, "signUpButton", "signup");
}

export function setupSignUp() {
  const signUpButton = document.getElementById("signUpButton");

  signUpButton.addEventListener("click", async () => {
    const qrCode = await fetchOtpSignUp();
    if (qrCode == null) {
      return;
    }

    stateManager.setState({ qr: qrCode });
    stateManager.setState({
      username: document.getElementById("username").value,
    });
    SPA.navigate("/signup-verify");
  });
}

async function fetchOtpSignUp() {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/signup";
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

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
