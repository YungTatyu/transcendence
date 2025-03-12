import fetchOtpSignUpVerify from "../api/fetchOtpSignUpVerify.js";
import fetchUpdateEmail from "../api/fetchUpdateEmail.js";
import Form from "../components/Form.js";
import generateVerifyForm from "../components/verifyForm.js";
import stateManager from "../stateManager.js";

export default function SignUpVerify() {
  const formHtml = generateVerifyForm(
    true,
    "Scan this QRcode and verify OTP",
    "signUpVerifyButton",
  );
  const updateEmailFormFields = [
    { label: "NewEmail", type: "email", placeholder: "abc@example.com" },
  ];
  const updateEmailFormHtml = Form(
    updateEmailFormFields,
    "updateEmail",
    "update-mail",
  );
  return formHtml + updateEmailFormHtml;
}

export function setupSignUpVerify() {
  const signUpVerifyButton = document.getElementById("signUpVerifyButton");
  const imgElement = document.getElementById("qrCode");
  const errorOutput = document.getElementById("errorOutput");

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
    const { status, data } = await fetchOtpSignUpVerify(username, otp);

    if (status === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status >= 400) {
      errorOutput.textContent = JSON.stringify(data.error, null, "\n");
      return;
    }
    console.log(data);

    // INFO stateManagerにuserIdを登録
    stateManager.setState({ userId: data.userId });

    const updateEmailButton = document.getElementById("updateEmail");
    updateEmailButton.addEventListener("click", async () => {
      const email = document.getElementById("fieldNewEmail").value;
      const { status, data } = await fetchUpdateEmail(email);

      if (status === null) {
        errorOutput.textContent = "Error Occured!";
        return;
      }
      if (status >= 400) {
        errorOutput.textContent = JSON.stringify(data.error, null, "\n");
        return;
      }
      console.log(data);
    });
  });
}
