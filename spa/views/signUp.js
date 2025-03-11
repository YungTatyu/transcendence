import fetchOtpSignUp from "../api/fetchOtpSignUp.js";
import generateForm from "../components/form.js";
import stateManager from "../stateManager.js";

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
    const username = document.getElementById("fieldUsername").value;
    const password = document.getElementById("fieldPassword").value;
    const email = document.getElementById("fieldMail").value;

    const { _, data } = await fetchOtpSignUp(username, password, email);

    if (data === null) {
      return;
    }

    stateManager.setState({ qr: data.qr_code });
    stateManager.setState({
      username: document.getElementById("fieldUsername").value,
    });
    SPA.navigate("/signup-verify");
  });
}
