import fetchApiWithBody from "../api/fetchApiWithBody.js";
import ChangeInfoForm from "../components/ChangeInfoForm.js";
import config from "../config.js";
import SPA from "../spa.js";

export default function ChangePassword() {
  const ChangePasswordFormField = [
    { label: "CurrentPass", type: "Password", placeholder: "password123" },
    { label: "NewPass", type: "Password", placeholder: "password123" },
  ];
  return ChangeInfoForm(
    ChangePasswordFormField,
    "changePassword",
    "Submit",
    "Set Your Password",
  );
}

export function setupChangePassword() {
  const submitButton = document.getElementById("changePassword");

  submitButton.addEventListener("click", async (event) => {
    event.preventDefault();
    const currentPass = document
      .getElementById("fieldCurrentPass")
      .value.trim();
    const newPass = document.getElementById("fieldNewPass").value.trim();
    const errorOutput = document.getElementById("errorOutput");

    if (!currentPass || !newPass) {
      alert("パスワードを入力してください");
      return;
    }

    const requestBody = {
      // biome-ignore lint/style/useNamingConvention :reason: "snake_case" is used in the API
      current_password: currentPass,
      // biome-ignore lint/style/useNamingConvention :reason: "snake_case" is used in the API
      new_password: newPass,
    };

    const { status, data } = await fetchApiWithBody(
      "PUT",
      config.authService,
      "/auth/me/password",
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
    SPA.navigate("/profile");
  });
}
