import fetchOtpLogin from "../api/fetchOtpLogin.js";
import generateForm from "../components/form.js";
import stateManager from "../stateManager.js";

export default function Login() {
  const loginFormFields = [
    { label: "Mail", type: "email", placeholder: "sample@example.com" },
    { label: "Password", type: "password", placeholder: "password123" },
  ];
  return generateForm(loginFormFields, "loginButton", "Login");
}

export function setupLogin() {
  const loginButton = document.getElementById("loginButton");
  const errorOutput = document.getElementById("errorOutput");

  loginButton.addEventListener("click", async () => {
    const email = document.getElementById("fieldMail").value;
    const password = document.getElementById("fieldPassword").value;

    const { status, data } = await fetchOtpLogin(email, password);
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
    SPA.navigate("/login-verify");
  });
}
