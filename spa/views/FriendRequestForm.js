import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendRequestForm() {
  let formContent = "";
  formContent += `
      <div class="mb-3">
        <label class="form-label">Find Your Friend</label>
			  <div class="d-flex gap-3">
				  <input type="username" class="form-control" id="field-username" required>
				  <button id="search-button" class="btn btn-primary btn-lg" type="button">
				    search
				  </button>
			  </div>
      </div>
        `;

  const formHtml = `
		<div class="container d-flex justify-content-center align-items-center vh-100 position-relative" style="max-width: 400px;">
		  <img src="/assets/batsu.png" alt="batsu" class="position-absolute end-0" style="top: 35%; width: 30px; height: 30px;">
		  <div class="card shadow-lg p-4" style="width: 100%; max-width: 400px;">
			<form class="rounded-pill text-center">
			  ${formContent}
			  <div>
				<p id="result-output" class="text-center text-danger fw-bold fs-6"></p>
			  </div>
			</form>
		  </div>
		</div>
	  `;
  return formHtml;
}

export function setupFriendRequestForm() {
  const searchButton = document.getElementById("search-button");
  let previousUsername = "";

  searchButton.addEventListener("click", async () => {
    const username = document.getElementById("field-username").value;
    const resultOutput = document.getElementById("result-output");
    // /user?username=usernameを叩いてuserIdに変換

    //formに入力されたusernameが同じまたは複数回serachボタンを押した時、再び,apiを叩かないようにする
    if (!username || previousUsername === username) return;
    previousUsername = username;
    resultOutput.textContent = "";

    // /friends/requests/useridを叩く
    // const { status, data } = await fetchApiWithBody(
    // 	"POST"
    // )

    const status = 200;
    const errorData = {
      error: "Error Now",
    };
    const data = {
      username: "test",
      avatarPath: "/assets/42.png",
    };

    if (status === null) {
      resultOutput.textContent = "Error Occured!";
      return;
    }
    if (status >= 400) {
      resultOutput.textContent = errorData.error;
      return;
    }
    resultOutput.appendChild(createUserCard(data));

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

      addButton.addEventListener("click", () =>
        handleAddFriend(addButton, addMessage),
      );

      divContainer.append(userImgContainer, usernameContainer);

      const wrapper = document.createElement("div");
      wrapper.append(divContainer, addButton, addMessage);
      return wrapper;
    }

    function handleAddFriend(button, message) {
      //リクエストを送る(api)
      const fDataError = {
        error: "already friend",
      };
      const fStatus = 400;
      if (fStatus >= 400)
        if (!message.textContent) message.textContent = fDataError.error;
        else {
          message.style.color = "#0B7D90";
          button.classList.replace("btn-primary", "btn-secondary");
          button.textContent = "added";
          if (!message.textContent)
            message.textContent = "Sent friend request.";
        }
    }
  });
}
