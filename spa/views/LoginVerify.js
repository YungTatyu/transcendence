import fetchApiWithBody from "../api/fetchApiWithBody.js";
import VerifyForm from "../components/VerifyForm.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function LoginVerify() {
  const formHtml = VerifyForm(false, "Verify OTP", "loginVerifyButton");
  return formHtml;
}

export function setupLoginVerify() {
  const loginVerifyButton = document.getElementById("loginVerifyButton");
  const errorOutput = document.getElementById("errorOutput");
  const email = stateManager.state.email;

  // INFO /login/verifyに直接アクセスされた場合に/loginにリダイレクト
  if (email === undefined) {
    SPA.navigate("/login");
    return;
  }

  loginVerifyButton.addEventListener("click", async () => {
    const otpInputs = document.querySelectorAll(".otp-input");
    const otp = Array.from(otpInputs)
      .map((input) => input.value)
      .join("");
    const requestBody = { email: email, otp: otp };

    const { status, data } = await fetchApiWithBody(
      "POST",
      config.authService,
      "/auth/otp/login/verify",
      requestBody,
    );

    if (status === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status >= 400) {
      errorOutput.textContent = JSON.stringify(data.error, null, "\n");
      return;
    }

    // INFO stateManagerにuserIdを登録
    stateManager.setState({ userId: data.userId });

    // INFO JWTが必要なユーザー名の更新エンドポイントを叩く
    const newName = Math.random()
      .toString(36)
      .slice(2, 2 + 9);

    const { status: status2, data: data2 } = await fetchApiWithBody(
      "PUT",
      config.userService,
      "/users/me/username",
      { username: newName },
    );

    if (status2 === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status2 >= 400) {
      errorOutput.textContent = JSON.stringify(data2.error, null, "\n");
      return;
    }
  });
}
