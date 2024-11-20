import { postData } from "./api.js";
import { BACKEND_IP_ADDRESS } from "./constants.js";

async function createAccount(event) {
  event.preventDefault()
  const username = document.querySelector(".js-create-username").value
  const email = document.querySelector(".js-create-mailaddress").value
  const password = document.querySelector(".js-create-password").value

  const response = await postData(`${BACKEND_IP_ADDRESS}/users/create/`, {
    username: username,
    email: email,
    password: password,
  })
  if (response === null) {
    alert("アカウント作成に失敗しました")
    return
  }

  console.log("login res=", response)
  localStorage.setItem('token', response.token);
  localStorage.setItem('userId', response.id);
  localStorage.setItem('username', response.username);
  window.location.href = "index.html"; // ログイン後のページ
}
document.querySelector(".js-form-create-user").addEventListener("submit", createAccount)
