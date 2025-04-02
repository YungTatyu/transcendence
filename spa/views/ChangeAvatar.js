import fetchApiNoBody from "../api/fetchApiNoBody.js";
import config from "../config.js";
import SPA from "../spa.js";
import stateManager from "../stateManager.js";

export default function ChangeAvatar() {
  return `
        <div class="container d-flex justify-content-center align-items-center vh-100">
          <div class="card shadow-lg p-4 align-items-center" style="width: 100%; max-width: 400px;">
            <form>    
              <img src="${config.userService}/media/images/default/default_image.png" class="square-img-user-avatar rounded-circle mb-3 js-new-avatar" >
               
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

async function fetchAvatarApi(method, baseUrl, endpoint, requestBody) {
  try {
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method,
      credentials: "include",
      body: requestBody,
    });

    const status = response.status;
    const data = await response.json();
    return { status, data };
  } catch (error) {
    console.error(`API fetch error at ${endpoint}:`, error);
    return { status: null, data: null };
  }
}

// Avatarをアップロードする処理
async function handleEditAvatar(fileInput, avatarImage) {
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("avatar_path", file);

  const { status, data } = await fetchAvatarApi(
    "PUT",
    config.userService,
    "/users/me/avatar",
    formData,
  );

  if (status === null || status >= 400) {
    console.error("アバター画像のアップロードに失敗しました");
    return;
  }

  const newAvatarUrl = `${config.userService}${data.avatarPath}`;

  avatarImage.src = newAvatarUrl;
  stateManager.setState({ avatarUrl: newAvatarUrl });
  SPA.navigate("/profile");
}

// Avatarを削除する処理
async function handleDeleteAvatar(avatarImage) {
  const { status, data } = await fetchApiNoBody(
    "DELETE",
    config.userService,
    "/users/me/avatar",
  );

  if (status === null || status >= 400) {
    console.error("アバター画像の削除に失敗しました");
    return;
  }
  stateManager.setState({ avatarUrl: `${config.userService}/media/images/default/default_image.png` });
  SPA.navigate("/profile");
}

export async function setupChangeAvatar() {
  const deleteButton = document.querySelector(".js-delete-avatar");
  const editButton = document.querySelector(".js-edit-avatar");
  const fileInput = document.querySelector(".js-avatar-input");
  const avatarImage = document.querySelector(".js-new-avatar");

  // Editボタン
  editButton.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () =>
    handleEditAvatar(fileInput, avatarImage),
  );

  // Deleteボタン
  deleteButton.addEventListener("click", () => handleDeleteAvatar(avatarImage));

  if (stateManager.state.avatarPath) {
    avatarImage.src = stateManager.state.avatarPath;
  } else {
    const { status, data } = await fetchApiNoBody(
      "GET",
      config.userService,
      `/users?userid=${stateManager.state.userId}`,
    );

    if (status === null || status >= 400) {
      console.error("ユーザー情報の取得に失敗しました");
      return;
    }
    const avatarUrl = `${config.userService}${data.avatarPath}`;
    avatarImage.src = avatarUrl;
    stateManager.setState({ avatarUrl: avatarUrl });
  }
}
