export default function VerifyForm(useQr, message, buttonId, otpSize = 6) {
  let formContent = "";

  if (useQr) {
    formContent += `
      <div class="d-flex justify-content-center align-items-center">
        <img id="qrCode" alt="QR Code" class="w-50">
      </div>`;
  }
  formContent += `
      <div class="d-flex justify-content-center align-items-center">
        <p class="text-dark fw-bold mt-3">
          ${message}
        </p>
       </div>`;

  let otpInput = "";
  for (let i = 0; i < otpSize; i++) {
    otpInput += `<input type="text" class="form-control text-center otp-input" maxlength="1" style="width: 50px; height: 50px;">`;
  }

  formContent += `
    <div class="container mt-4">
      <div class="d-flex justify-content-center gap-2">${otpInput}</div>
    </div>`;

  const formHtml = `
    <div class="container d-flex justify-content-center align-items-center vh-100">
      <div class="gradient-border-wrapper">
        <div class="form-wrapper">
          <form onsubmit="return false;">
            ${formContent}
            <div class="text-center mt-3">
              <button id="${buttonId}" class="btn btn-primary btn-lg form-btn" type="button">Verify</button>
            </div>
            <div class="mt-5">
              <p id="errorOutput" class="text-center text-danger fw-bold fs-6"></p>
            </div>
          </form>
        </div>
      </div>
    </div>`;

  // フォームが生成された後にイベントリスナーを適用
  setTimeout(() => setupOtpInputs(buttonId), 0);

  return formHtml;
}

// OTP 入力欄のイベントリスナーを設定
function setupOtpInputs(buttonId) {
  const inputs = document.querySelectorAll(".otp-input");
  const verifyButton = document.getElementById(buttonId);

  inputs.forEach((input, index) => {
    input.addEventListener("input", (e) => {
      if (e.target.value.length === 1) {
        if (index < inputs.length - 1) {
          inputs[index + 1].focus(); // 次の入力欄に移動
        } else {
          // 最後の入力欄が入力されたらVerify ボタンにフォーカスを移動
          e.preventDefault();
          verifyButton.focus();
        }
      }
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && index > 0 && input.value === "") {
        inputs[index - 1].focus(); // バックスペースで前の入力欄に戻る
      }
    });
  });
}
