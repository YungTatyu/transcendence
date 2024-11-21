
import { fetchData, postData } from "../js/api.js"; // パスは実際のパスに合わせてください

// モック関数
jest.mock("../js/api.js", () => ({
  fetchData: jest.fn(),
  postData: jest.fn(),
}));

describe("Note form", () => {
  beforeEach(async () => {
    // テスト用HTMLのセットアップ
    document.body.innerHTML = `
      <form class="js-note-container">
        <input type="text" class="js-form-title" />
        <textarea class="js-form-content"></textarea>
      </form>
    `;

    // モックレスポンス設定
    fetchData.mockResolvedValue({ title: "Test Note", content: "Test content" });
    postData.mockResolvedValue({ success: true });

    // window.location.href のモック化
    delete window.location;
    window.location = { href: "" };
  });

  test("renderNoteValue sets form values from URL params", async () => {
    // URLパラメータをセット
    global.URLSearchParams = jest.fn(() => ({
      get: jest.fn(() => "1"),
      size: 1,
    }));

    const { renderNoteValue, handleResponse, save } = await import("../js/edit_note.js");
    // ここで login をグローバルに利用可能にする
    global.renderNoteValue = renderNoteValue
    global.handleResponse = handleResponse
    global.save = save
    // モックされた fetchData を呼び出してフォームにタイトルと内容を設定
    await renderNoteValue();

    // フォームに値が設定されているか確認
    const titleInput = document.querySelector(".js-form-title");
    const contentInput = document.querySelector(".js-form-content");

    expect(titleInput.value).toBe("Test Note");
    expect(contentInput.value).toBe("Test content");
  });

  // test("save calls postData with correct parameters when creating a new note", async () => {
  //   // URLパラメータがない場合のテスト
  //   global.URLSearchParams = jest.fn().mockImplementation(() => ({
  //     size: 0,
  //     get: jest.fn().mockReturnValue(null), // noteId が無い場合、null を返す
  //   }));
  //
  //   const { renderNoteValue, handleResponse, save } = await import("../js/edit_note.js");
  //   const form = document.querySelector(".js-note-container");
  //   const titleInput = document.querySelector(".js-form-title");
  //   const contentInput = document.querySelector(".js-form-content");
  //
  //   titleInput.value = "New Note";
  //   contentInput.value = "New content";
  //
  //   // フォーム送信をシミュレート
  //   const event = new Event("submit");
  //   await save(event);
  //
  //   // postData が正しい引数で呼ばれたか確認
  //   expect(postData).toHaveBeenCalledWith(
  //     "http://127.0.0.1:8000/notes/create/",
  //     { title: "New Note", content: "New content" }
  //   );
  // });

  test("save calls postData with correct parameters when updating an existing note", async () => {
    // URLパラメータが存在する場合のテスト
    global.URLSearchParams = jest.fn(() => ({
      noteId: jest.fn(() => "1"),
      size: 1,
    }));

    const { renderNoteValue, handleResponse, save } = await import("../js/edit_note.js");
    const form = document.querySelector(".js-note-container");
    const titleInput = document.querySelector(".js-form-title");
    const contentInput = document.querySelector(".js-form-content");

    titleInput.value = "Updated Note";
    contentInput.value = "Updated content";

    // フォーム送信をシミュレート
    const event = new Event("submit");
    await save(event);

    // postData が正しい引数で呼ばれたか確認
    expect(postData).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/notes/update/1/",
      { title: "Updated Note", content: "Updated content" },
      "PUT"
    );
  });

  test("handleResponse shows an alert if response is null", async () => {
    // alert をモック化
    window.alert = jest.fn();
    const { renderNoteValue, handleResponse, save } = await import("../js/edit_note.js");

    // handleResponse をテスト
    handleResponse(null);

    // アラートが呼ばれたか確認
    expect(window.alert).toHaveBeenCalledWith("ノートの保存に失敗しました。");
  });

  test("handleResponse redirects when response is not null", async () => {
    // handleResponse をテスト
    const { renderNoteValue, handleResponse, save } = await import("../js/edit_note.js");
    handleResponse({ success: true });

    // window.location.href が変更されたか確認
    expect(window.location.href).toBe("index.html");
  });
});
