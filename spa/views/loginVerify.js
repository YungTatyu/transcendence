import fetchOtpLoginVerify from "../api/fetchOtpLoginVerify.js";
import fetchUpdateUserName from "../api/fetchUpdateUserName.js";
import generateVerifyForm from "../components/verifyForm.js";
import stateManager from "../stateManager.js";

export default function SignUp() {
  const formHtml = generateVerifyForm(false, "Verify OTP", "loginVerifyButton");
  return formHtml;
}

export function setupLoginVerify() {
  const loginVerifyButton = document.getElementById("loginVerifyButton");
  const errorOutput = document.getElementById("errorOutput");
  const email = stateManager.state.email;

  // INFO /login-verifyに直接アクセスされた場合に/loginにリダイレクト
  if (email === undefined) {
    SPA.navigate("/login");
    return;
  }

  loginVerifyButton.addEventListener("click", async () => {
    const otpInputs = document.querySelectorAll(".otp-input");
    const otp = Array.from(otpInputs)
      .map((input) => input.value)
      .join("");
    const { status, data } = await fetchOtpLoginVerify(email, otp);

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

    // INFO JWTが必要なユーザー名の更新エンドポイントを叩く
    const newName = Math.random()
      .toString(36)
      .slice(2, 2 + 9);

    const { status: status2, data: data2 } = await fetchUpdateUserName(newName);

    if (status2 === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status2 >= 400) {
      errorOutput.textContent = JSON.stringify(data2.error, null, "\n");
      return;
    }
    console.log(data2);
  });
}
