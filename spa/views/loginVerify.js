import generateVerifyForm from "../components/verifyForm.js";

export default function SignUp() {
  const formHtml = generateVerifyForm(false, "Verify OTP", "loginVerifyButton");
  return formHtml;
}

export function setupLoginVerify() {
  const loginVerifyButton = document.getElementById("loginVerifyButton");

  loginVerifyButton.addEventListener("click", async () => {});
}
