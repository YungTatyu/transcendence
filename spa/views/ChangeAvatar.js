import fetchApiNoBody from "../api/fetchApiNoBody.js";
import fetchApiWithBody from "../api/fetchApiWithBody.js";
import config from "../config.js";

export default function ChangeAvatar() {
  return `
        <div class="container d-flex justify-content-center align-items-center vh-100">
          <div class="card shadow-lg p-4 align-items-center" style="width: 100%; max-width: 400px;">
            <form>    
              <img id="user-avatar" src="/assets/user.png" class="square-img-user-avatar rounded-circle mb-3 js-new-avatar" >
               
              <!-- 隠しファイル入力 -->
              <input type="file" class="js-avatar-input d-none" accept="image/*">
          
              <div class="d-flex gap-2 mt-4">
                <button class="btn btn-primary w-50 js-edit-avatar" type="button">Edit</button>
                <button class="btn btn-danger w-50 js-delete-avatar" type="button">Delete</button>
              </div>
            </form>
          </div>
        </div>
      `;
}

export function setupChangeAvatar() {
  const deleteButton = document.querySelector(".js-delete-avatar");
  const editButton = document.querySelector(".js-edit-avatar");
  const fileInput = document.querySelector(".js-avatar-input");
  const avatarImage = document.getElementById("js-new-avatar");

  // Editボタンを押したらファイル選択ウィンドウを開く
  editButton.addEventListener("click", () => {
    fileInput.click();
  });

  // ファイルが選択されたらアップロード処理
  fileInput.addEventListener("change", async (event) => {
    //選択されたファイルを取得
    const file = event.target.files[0];
    if (!file) return;
    //multipart/form-dataで送信できるようにformを作成
    const formData = new FormData();
    formData.append("avatar_path", file);

    const { status, data } = await fetchApiWithBody(
      "PUT",
      config.userService,
      "/users/me/avatar",
      formData,
    );

    if (status === null || status >= 400) {
      console.error("アバター画像のアップロードに失敗しました");
      return;
    }

    avatarImage.src = data.avatarPath;
  });

  // Deleteボタン
  deleteButton.addEventListener("click", async () => {
    const { status, data } = await fetchApiNoBody(
      "DELETE",
      config.userService,
      "/users/me/avatar",
    );

    if (status === null || status >= 400) {
      console.error("アバター画像の削除に失敗しました");
      return;
    }
  });
}
