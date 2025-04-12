import fetchApiWithBody from "../api/fetchApiWithBody.js";
import VerifyForm from "../components/VerifyForm.js";
import config from "../config.js";
import WsFriendActivityManager from "../services/friend_activity/WsFriendActivityManager.js";
import stateManager from "../stateManager.js";
import { parseJwt, scheduleRefresh } from "../utils/jwtHelper.js";

export default function SignUpVerify() {
  return VerifyForm(
    true,
    "Scan this QRcode and verify OTP",
    "signUpVerifyButton",
  );
}

export function setupSignUpVerify() {
  const signUpVerifyButton = document.getElementById("signUpVerifyButton");
  const imgElement = document.getElementById("qrCode");
  const errorOutput = document.getElementById("errorOutput");

  const username = stateManager.state.username;
  const qrCode = stateManager.state.qr;

  // INFO /signup/verifyに直接アクセスされた場合に/signupにリダイレクト
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

    const requestBody = { username: username, otp: otp };
    const { status, data } = await fetchApiWithBody(
      "POST",
      config.authService,
      "/auth/otp/signup/verify",
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
