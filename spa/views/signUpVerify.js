import fetchOtpSignUpVerify from "../api/fetchOtpSignUpVerify.js";
import fetchUpdateEmail from "../api/fetchUpdateEmail.js";
import generateForm from "../components/form.js";
import generateVerifyForm from "../components/verifyForm.js";
import stateManager from "../stateManager.js";

export default function SignUpVerify() {
  const formHtml = generateVerifyForm(
    true,
    "Scan this QRcode and verify OTP",
    6,
    "signUpVerifyButton",
  );
  const updateEmailFormFields = [
    { label: "NewEmail", type: "email", placeholder: "abc@example.com" },
  ];
  const updateEmailFormHtml = generateForm(
    updateEmailFormFields,
    "updateEmail",
    "update-mail",
  );
  return formHtml + updateEmailFormHtml;
}

export function setupSignUpVerify() {
  const signUpVerifyButton = document.getElementById("signUpVerifyButton");
  const imgElement = document.getElementById("qrCode");

  const username = stateManager.state.username;
  const qrCode = stateManager.state.qr;

  // INFO /signup-verifyに直接アクセスされた場合に/signupにリダイレクト
  if (qrCode === undefined || username === undefined) {
    SPA.navigate("/signup");
    return;
  }

  imgElement.src = qrCode;

  signUpVerifyButton.addEventListener("click", async () => {
    const otpInputs = document.querySelectorAll(".otp-input"); // すべての要素を取得
    const otp = Array.from(otpInputs)
      .map((input) => input.value)
      .join("");
    const { _, data } = await fetchOtpSignUpVerify(username, otp);

    if (data === null) {
      return;
    }
    console.log(data);

    const updateEmailButton = document.getElementById("updateEmail");
    updateEmailButton.addEventListener("click", async () => {
      const email = document.getElementById("fieldNewEmail").value;
      const { _, data } = await fetchUpdateEmail(email);
      if (data === null) {
        return;
      }
      console.log(data);
    });
  });
}
