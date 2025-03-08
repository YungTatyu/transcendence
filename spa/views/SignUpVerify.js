import Footer from "../components/Footer.js";
import Header from "../components/Header.js";
import stateManager from "../stateManager.js";

export default function SignUp() {
	return `
    ${Header({ title: "signup" })}
    <img id="qrCodeImage" alt="QR Code">
    <button id="signUpVerifyButton">verify</button>
    ${Footer({ text: "© 2025 My Company" })}
  `;
}

export function setupSignUpVerify() {
	const signUpVerifyButton = document.getElementById("signUpVerifyButton");

	document.getElementById("qrCodeImage").src = stateManager.state.qr;

	signUpVerifyButton.addEventListener("click", () => {
		const resData = fetchOtpSignUpVerify();
		if (resData == null) { return; }
		console.log(resData);
	});
}

async function fetchOtpSignUpVerify() {
	const AUTH_API_BASE_URL = "http://localhost:8000";
	const ENDPOINT = "/auth/otp/signup/verify";

	const requestBody = {
		username: stateManager.state.username,
		otp: document.getElementById("otp"),
	};

	try {
		const response = await fetch(`${AUTH_API_BASE_URL}${ENDPOINT}`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(requestBody)
		});

		if (!response.ok) {
			throw new Error(`HTTP Error! Status: ${response.status}`);
		}

		const resData = await response.json();
		return resData;
	} catch (error) {
		console.error("API fetch error: ", error);
		return null;
	}
}
