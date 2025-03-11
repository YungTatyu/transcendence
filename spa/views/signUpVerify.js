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
    {
      label: "NewEmail",
      type: "email",
      placeholder: "abc@example.com",
      required: true,
    },
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

  const qrCode = stateManager.state.qr;
  const imgElement = document.getElementById("qrCode");
  imgElement.src = qrCode;

  signUpVerifyButton.addEventListener("click", async () => {
    const username = stateManager.state.username;
    const otpInputs = document.querySelectorAll(".otp-input"); // すべての要素を取得
    const otp = Array.from(otpInputs)
      .map((input) => input.value)
      .join("");
    const resData = await fetchOtpSignUpVerify(username, otp);
    if (resData == null) {
      return;
    }
    console.log(resData);

    const updateEmailButton = document.getElementById("updateEmail");
    updateEmailButton.addEventListener("click", async () => {
      const email = document.getElementById("fieldNewEmail").value;
      const resData = await fetchUpdateEmail(email);
      if (resData == null) {
        return;
      }
      console.log(resData);
    });
  });
}
