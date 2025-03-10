import stateManager from "../stateManager.js";

export default function SignUp() {
  return `
	<div class="container d-flex justify-content-center align-items-center vh-100">
		<div class="card shadow-lg p-4" style="width: 100%; max-width: 400px;">
			<form class="rounded-pill">
				<div class="mb-3">
					<label for="username" class="form-label">Username</label>
					<input type="text"  class="form-control" id="username" name="username" required>
				</div>

				<div class="mb-3">
					<label for="password" class="form-label">Password</label>
					<input type="password"  class="form-control" id="password" name="password" required>
				</div>
        
				<div class="mb-3">
					<label for="email" class="form-label">Mail</label>
					<input type="email"  class="form-control" id="email" name="email" required>
				</div>

				<div class="text-end">
					<button id="signUpButton" class="btn btn-primary btn-lg">signup</button>
				</div>
			</form>
		</div>
	</div>
  `;
}

export function setupSignUp() {
  const signUpButton = document.getElementById("signUpButton");

  signUpButton.addEventListener("click", async () => {
    const qrCode = await fetchOtpSignUp();
    if (qrCode == null) {
      return;
    }

    stateManager.setState({ qr: qrCode });
    stateManager.setState({
      username: document.getElementById("username").value,
    });
    SPA.navigate("/signup-verify");
  });
}

async function fetchOtpSignUp() {
  const authApiBaseUrl = "http://localhost:8000";
  const endpoint = "/auth/otp/signup";
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const requestBody = { username: username, email: email, password: password };

  try {
    const response = await fetch(`${authApiBaseUrl}${endpoint}`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error! Status: ${response.status}`);
    }

    const resData = await response.json();
    return resData.qr_code;
  } catch (error) {
    console.error("API fetch error: ", error);
    return null;
  }
}
