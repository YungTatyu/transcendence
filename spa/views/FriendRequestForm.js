import fetchApiNoBody from "../api/fetchApiNoBody.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendRequestForm() {
  const formContent = `
    <div class="mb-3">
      <label class="form-label">Find Your Friend</label>
			<div class="d-flex gap-3">
				<input type="text" class="form-control" id="field-username" required>
				<button id="search-button" class="btn btn-primary btn-lg" type="button">
				  search
				</button>
			</div>
    </div>
        `;

  return `
		<div class="container d-flex justify-content-center align-items-center vh-100 position-relative" style="max-width: 400px;">
		  <div class="card shadow-lg p-4" style="width: 100%; max-width: 400px;">
            <div class="position-absolute" style="top: -25px; right: -60px;">
              <img src="/assets/batsu.png" alt="batsu" style="width: 40px; height: 40px;" onclick="SPA.navigate('/home')">
            </div>
			<form class="rounded-pill text-center">
			  ${formContent}
			  <div>
				<p id="result-output" class="text-center text-danger fw-bold fs-6"></p>
			  </div>
			</form>
		  </div>
		</div>
	  `;
}

export function setupFriendRequestForm() {
  const searchButton = document.getElementById("search-button");
  let previousUsername = "";

  searchButton.addEventListener("click", async () => {
    const username = document.getElementById("field-username").value;
    const resultOutput = document.getElementById("result-output");
    //formに入力されたusernameが同じまたは複数回serachボタンを押した時、再び,apiを叩かないようにする
    if (!username || previousUsername === username) return;
    previousUsername = username;
    resultOutput.textContent = "";

    // 自身にリクエストを送る時、friend/requestではなく/user?username=usernameの前にエラー処理
    const setedUsername = stateManager.state?.username;
    if (setedUsername === username) {
      resultOutput.textContent = "You cannot send a request to yourself.";
      return;
    }
    // /user?username=usernameを叩いてuserIdに変換
    const userInfo = await fetchApiNoBody(
      "GET",
      config.userService,
      `/users?username=${username}`,
    );
    if (userInfo.status == null) {
      resultOutput.textContent = "Error Occured!";
      return;
    }
    if (userInfo.status >= 400) {
      resultOutput.textContent = JSON.stringify(
        userInfo.data.error,
        null,
        "\n",
      );
      return;
    }

    function createUserCard(data) {
      const divContainer = document.createElement("div");
      divContainer.classList.add("d-flex", "gap-3", "align-items-center");

      const userImgContainer = document.createElement("img");
      Object.assign(userImgContainer.style, {
        width: "50px",
        height: "50px",
        objectFit: "cover",
        borderRadius: "50%",
      });
      userImgContainer.src = data.avatarPath;

      const usernameContainer = document.createElement("div");
      usernameContainer.classList.add("text-dark", "fs-5");
      usernameContainer.textContent = data.username;

      const addButton = document.createElement("button");
      addButton.classList.add("btn", "btn-primary", "btn-lg");
      addButton.textContent = "add";
      addButton.type = "button";

      const addMessage = document.createElement("div");
      addMessage.textContent = "";

      addButton.addEventListener(
        "click",
        async () => await handleAddFriend(addButton, addMessage),
      );

      divContainer.append(userImgContainer, usernameContainer);

      const wrapper = document.createElement("div");
      wrapper.append(divContainer, addButton, addMessage);
      return wrapper;
    }

    async function handleAddFriend(button, message) {
      //リクエストを送る(api)
      const requestInfo = await fetchApiNoBody(
        "POST",
        config.friendService,
        `/friends/requests/${userInfo.data.userId}`,
      );
      if (requestInfo.status >= 400) {
        message.textContent = JSON.stringify(
          requestInfo.data.error,
          null,
          "\n",
        );
      } else {
        message.style.color = "#0B7D90";
        button.classList.replace("btn-primary", "btn-secondary");
        button.textContent = "added";
        message.textContent = "Sent friend request.";
      }
    }

    resultOutput.appendChild(createUserCard(userInfo.data));
  });
}
