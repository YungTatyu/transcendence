export default function generateVerifyForm(useQr, message, otpSize, buttonId) {
  let formContent = "";

  if (useQr) {
    formContent += `
			<div class="d-flex justify-content-center align-items-center">
				<img id="qrCode" alt="QR Code" class="w-50">
			</div>
		`;
  }
  formContent += `<div class="d-flex justify-content-center align-items-center"><p>${message}</p></div>`;

  for (let i = 0; i < otpSize; i++) {
    formContent += `<input type="text" class="form-control digit-input" maxlength="1">`;
  }

  const formHtml = `
		<div class="container d-flex justify-content-center align-items-center vh-100">
			<div class="card shadow-lg p-4" style="width: 100%; max-width: 400px;">
				<form class="rounded-pill">
					${formContent}
					<div class="text-end">
						<button id="${buttonId}" class="btn btn-primary btn-lg" type="button">Verify</button>
					</div>
				</form>
			</div>
		</div>
	`;
  return formHtml;
}
