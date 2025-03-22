import fetchApiWithBody from "../api/fetchApiWithBody.js";
import Form from "../components/Form.js";
import config from "../config.js";
import SPA from "../spa.js";
import stateManager from "../stateManager.js";

export default function ChangeUsername() {
  const ChangeNameFormField = [
    { label: "Username", type: "username", placeholder: "New Username" },
  ];
  return Form(
    ChangeNameFormField,
    "changeUsername",
    "Submit",
    "Set Your Username",
  );
}

export function setupChageUsername() {
  const submitButton = document.getElementById("changeUsername");

  submitButton.addEventListener("click", async (event) => {
    event.preventDefault();
    const newUsername = document.getElementById("fieldUsername").value.trim();
    const errorOutput = document.getElementById("errorOutput");

    if (!newUsername) {
      alert("ユーザー名を入力してください");
      return;
    }

    const requestBody = {
      username: newUsername,
    };

    const { status, data } = await fetchApiWithBody(
      "PUT",
      config.userService,
      "/users/me/username",
      requestBody,
    );

    if (status === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    //一時的に409エラーようにおいてます。バックエンドのエラーフィールド名修正後に下の400以上のに統合予定
    if (status === 409) {
      errorOutput.textContent = JSON.stringify(data, null, "\n");
      return;
    }
    if (status >= 400) {
      errorOutput.textContent = JSON.stringify(data.error, null, "\n");
      return;
    }
    stateManager.setState({ username: newUsername });
    SPA.navigate("/profile");
  });
}
