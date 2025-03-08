import Footer from "../components/Footer.js";
import Header from "../components/Header.js";
import stateManager from "../stateManager.js";

export default function SignUp() {
  return `
    ${Header({ title: "signup" })}
	<label for="username">ユーザー名:</label>
    <input type="text" id="username" name="username" required><br><br>
        
    <label for="email">メールアドレス:</label>
    <input type="email" id="email" name="email" required><br><br>
        
    <label for="password">パスワード:</label>
    <input type="password" id="password" name="password" required><br><br>
    <button id="signUpButton">signup</button>
    ${Footer({ text: "© 2025 My Company" })}
  `;
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
