import { postData } from "./api.js";

async function login(event) {

  event.preventDefault(); // フォームのデフォルト動作を防ぐ

  const username = document.querySelector(".js-login-username").value
  const password = document.querySelector(".js-login-password").value
  const res = await postData("http://127.0.0.1:8000/users/login/", { username: username, password: password })
  if (res === null) {
    alert("ログインに失敗しました。");
    return
  }
  console.log("login res=", res)
  window.location.href = "index.html"; // ログイン後のページ
}

document.querySelector(".js-login-form").addEventListener("submit", login)
