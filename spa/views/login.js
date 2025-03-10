import generateForm from "../components/form.js";

export default function Login() {
  const loginFormFields = [
    {
      label: "Mail",
      type: "email",
      placeholder: "sample@example.com",
      required: true,
    },
    {
      label: "Password",
      type: "password",
      placeholder: "password123",
      required: true,
    },
  ];
  return generateForm(loginFormFields, "loginButton", "Login");
}

export function setupLogin() {
  const loginButton = document.getElementById("loginButton");

  loginButton.addEventListener("click", async () => {});
}
