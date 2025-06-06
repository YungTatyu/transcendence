import fetchApiWithBody from "../api/fetchApiWithBody.js";
import ChangeInfoForm from "../components/ChangeInfoForm.js";
import config from "../config.js";
import SPA from "../spa.js";

export default function ChangeMail() {
  const ChangeMailFormField = [
    { label: "Mail", type: "email", placeholder: "sample@example.com" },
  ];
  return ChangeInfoForm(
    ChangeMailFormField,
    "changeMail",
    "Submit",
    "Set Your Mail",
  );
}

export function setupChangeMail() {
  const submitButton = document.getElementById("changeMail");
  submitButton.addEventListener("click", async (event) => {
    event.preventDefault();
    const newMail = document.getElementById("fieldMail").value.trim();
    const errorOutput = document.getElementById("errorOutput");

    if (!newMail) {
      alert("メールアドレスを入力してください");
      return;
    }

    const requestBody = {
      email: newMail,
    };

    const { status, data } = await fetchApiWithBody(
      "PUT",
      config.authService,
      "/auth/me/email",
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
