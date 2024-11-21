import { postData } from "../js/api.js";

jest.mock("../js/api.js"); // APIモジュールをモック化

beforeEach(async () => {
  // テスト用HTMLをセットアップ
  document.body.innerHTML = `
    <form class="js-login-form">
      <input type="text" class="js-login-username" value="test-user" />
      <input type="password" class="js-login-password" value="test-pass" />
    </form>
  `;

  // localStorage をモック化
  Object.defineProperty(window, 'localStorage', {
    value: {
      setItem: jest.fn(),
    },
    writable: true,
  });

  // window.location.href をモック化
  delete window.location;
  window.location = { href: "" };

  // login.js を動的にインポート
  const { login } = await import("../js/login.js");
  // ここで login をグローバルに利用可能にする
  global.login = login;
});

afterEach(() => {
  jest.clearAllMocks(); // 各テスト後にモックをリセット
});

test("successful login sets localStorage and redirects", async () => {
  // postData のモックレスポンスを設定
  postData.mockResolvedValue({
    token: "mock-token",
    id: 1,
    username: "test-user",
  });

  const form = document.querySelector(".js-login-form");
  const event = new Event("submit");

  await login(event);

  // postData が正しい引数で呼び出されていることを確認
  expect(postData).toHaveBeenCalledWith("http://127.0.0.1:8000/users/login/", {
    username: "test-user",
    password: "test-pass",
  });

  // localStorage が正しく設定されていることを確認
  expect(localStorage.setItem).toHaveBeenCalledWith("token", "mock-token");
  expect(localStorage.setItem).toHaveBeenCalledWith("userId", 1);
  expect(localStorage.setItem).toHaveBeenCalledWith("username", "test-user");

  // リダイレクトが実行されていることを確認
  expect(window.location.href).toBe("index.html");
});

test("failed login shows alert", async () => {
  // postData が null を返すように設定
  postData.mockResolvedValue(null);

  // alert をモック化
  window.alert = jest.fn();

  const form = document.querySelector(".js-login-form");
  const event = new Event("submit");

  // login 関数を実行
  await login(event);

  // アラートが表示されていることを確認
  expect(window.alert).toHaveBeenCalledWith("ログインに失敗しました。");

  // localStorage やリダイレクトが行われていないことを確認
  expect(localStorage.setItem).not.toHaveBeenCalled();
  expect(window.location.href).toBe("");
});

