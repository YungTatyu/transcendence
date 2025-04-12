import fetchApiWithBody from "../api/fetchApiWithBody.js";
import VerifyForm from "../components/VerifyForm.js";
import config from "../config.js";
import WsFriendActivityManager from "../services/friend_activity/WsFriendActivityManager.js";
import stateManager from "../stateManager.js";
import { parseJwt, scheduleRefresh } from "../utils/jwtHelper.js";

export default function LoginVerify() {
  return VerifyForm(false, "Verify OTP", "loginVerifyButton");
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

    const accessToken = data.accessToken;
    // INFO stateManagerにuserIdを登録
    stateManager.setState({ userId: data.userId });
    sessionStorage.setItem("access_token", accessToken);
    scheduleRefresh(parseJwt(accessToken));
    try {
      WsFriendActivityManager.disconnect();
      WsFriendActivityManager.connect(accessToken);
    } catch (error) {
      console.error(error);
    }
    SPA.navigate("/home");
  });
}
