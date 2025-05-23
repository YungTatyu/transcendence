import fetchApiNoBody from "../api/fetchApiNoBody.js";
import config from "../config.js";
import SPA from "../spa.js";
import stateManager from "../stateManager.js";

export default function ChangeAvatar() {
  return `
    <div class="container d-flex justify-content-center align-items-center vh-100">
      <div class="gradient-border-wrapper">
        <div class="form-wrapper position-relative">
          <div class="close-btn-wrapper">
            <img src="/assets/batsu.png" alt="batsu" class="close-btn-img" onclick="SPA.navigate('/profile')">
          </div>
          <form>
            <div class="text-center">    
              <img src="${config.userService}/media/images/default/default_image.png" class="square-img-user-avatar rounded-circle mb-3 js-new-avatar" >
            </div>
            <!-- 隠しファイル入力 -->
            <input type="file" class="js-avatar-input d-none" accept="image/*">
            <div>
              <p class="text-center text-danger fw-bold fs-6 errorOutput"></p>
            </div>
        
            <div class="d-flex gap-2 mt-4">
              <button class="btn btn-primary btn-edit w-50 js-edit-avatar" type="button">Edit</button>
              <button class="btn btn-danger btn-delete w-50 js-delete-avatar" type="button">Delete</button>
            </div>
          </form>
        </div>
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
  const errorOutput = document.querySelector(".errorOutput");

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

  if (status === null) {
    errorOutput.textContent = "Error Occured!";
    return;
  }
  if (status >= 400) {
    errorOutput.textContent = JSON.stringify(data.error, null, "\n");
    return;
  }

  const newAvatarUrl = `${config.userService}${data.avatarPath}`;

  avatarImage.src = newAvatarUrl;
  stateManager.setState({ avatarUrl: newAvatarUrl });
  SPA.navigate("/profile");
}

// Avatarを削除する処理
async function handleDeleteAvatar() {
  const errorOutput = document.querySelector(".errorOutput");

  const { status, data } = await fetchApiNoBody(
    "DELETE",
    config.userService,
    "/users/me/avatar",
  );

  if (status === null) {
    errorOutput.textContent = "Error Occured!";
    return;
  }
  if (status >= 400) {
    errorOutput.textContent = JSON.stringify(data.error, null, "\n");
    return;
  }

  stateManager.setState({
    avatarUrl: `${config.userService}/media/images/default/default_image.png`,
  });
  SPA.navigate("/profile");
}

export async function setupChangeAvatar() {
  const deleteButton = document.querySelector(".js-delete-avatar");
  const editButton = document.querySelector(".js-edit-avatar");
  const fileInput = document.querySelector(".js-avatar-input");
  const avatarImg = document.querySelector(".js-new-avatar");

  if (!(deleteButton && editButton && fileInput && avatarImg)) {
    return;
  }
  // Editボタン
  editButton.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () =>
    handleEditAvatar(fileInput, avatarImg),
  );

  // Deleteボタン
  deleteButton.addEventListener("click", () => handleDeleteAvatar());

  if (stateManager.state.avatarUrl) {
    avatarImg.src = stateManager.state.avatarUrl;
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
    avatarImg.src = avatarUrl;
    stateManager.setState({ avatarUrl: avatarUrl });
  }
}
