import fetchOtpSignUp from "../api/fetchOtpSignUp.js";
import generateForm from "../components/form.js";
import stateManager from "../stateManager.js";

export default function SignUp() {
  const signUpFormFields = [
    { label: "Username", type: "text", placeholder: "User" },
    { label: "Password", type: "password", placeholder: "password123" },
    { label: "Mail", type: "email", placeholder: "sample@example.com" },
  ];
  return generateForm(signUpFormFields, "signUpButton", "signup");
}

export function setupSignUp() {
  const signUpButton = document.getElementById("signUpButton");
  const errorOutput = document.getElementById("errorOutput");

  signUpButton.addEventListener("click", async () => {
    const username = document.getElementById("fieldUsername").value;
    const password = document.getElementById("fieldPassword").value;
    const email = document.getElementById("fieldMail").value;

    const { status, data } = await fetchOtpSignUp(username, password, email);
    console.log(data);

    if (status === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status >= 400) {
      errorOutput.textContent = JSON.stringify(data.error, null, "\n");
      return;
    }

    stateManager.setState({ qr: data.qr_code });
    stateManager.setState({ username: username });
    SPA.navigate("/signup-verify");
  });
}
