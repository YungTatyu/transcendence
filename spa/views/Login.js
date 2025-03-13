import fetchApiWithBody from "../api/fetchApiWithBody.js";
import Form from "../components/Form.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function Login() {
  const loginFormFields = [
    { label: "Mail", type: "email", placeholder: "sample@example.com" },
    { label: "Password", type: "password", placeholder: "password123" },
  ];
  return Form(loginFormFields, "loginButton", "Login");
}

export function setupLogin() {
  const loginButton = document.getElementById("loginButton");
  const errorOutput = document.getElementById("errorOutput");

  loginButton.addEventListener("click", async () => {
    const email = document.getElementById("fieldMail").value;
    const password = document.getElementById("fieldPassword").value;
    const requestBody = {
      email: email,
      password: password,
    };

    const { status, data } = await fetchApiWithBody(
      "POST",
      config.authService,
      "/auth/otp/login",
      requestBody,
    );
    console.log(data);

    if (status === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status >= 400) {
      errorOutput.textContent = JSON.stringify(data.error, null, "\n");
      return;
    }

    stateManager.setState({ email: email });
    SPA.navigate("/login/verify");
  });
}
