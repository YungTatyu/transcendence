import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendRequestForm() {
	let formContent = "";
	formContent += `
          <div class="mb-3">
            <label class="form-label">Find Your Friend</label>
			<div class="d-flex gap-3">
				<input type="username" class="form-control" id="fieldUsername" required>
				<button id="searchButton" class="btn btn-primary btn-lg" type="button">
				  search
				</button>
			</div>
          </div>
        `;
	
		const formHtml = `
		<div class="container d-flex justify-content-center align-items-center vh-100">
		  <div class="card shadow-lg p-4" style="width: 100%; max-width: 400px; height: 300px;">
			<form class="rounded-pill text-center">
			  ${formContent}
			  <div>
				<p id="resultOutput" class="text-center text-danger fw-bold fs-6"></p>
			  </div>
			</form>
		  </div>
		</div>
	  `;
	return formHtml;
}

export function setupFriendRequestForm() {
	const searchButton = document.getElementById("searchButton");

	searchButton.addEventListener("click", async () => {
		const username = document.getElementById("fieldUsername").value;
		const resultOutput = document.getElementById("resultOutput");
		// /user?username=usernameを叩いてuserIdに変換

		resultOutput.textContent = "";

		// /friends/requests/useridを叩く
		// const { status, data } = await fetchApiWithBody(
		// 	"POST"
		// )

		//TODO
		//formに入力されたusernameが同じまたは複数回serachボタンを押した時、再び,apiを叩かないようにする

		const status = 200;
		const error_data = {
			"error": "Error Now", 
		}
		const data = {
			"username": "test",
			"avatarPath":"/assets/42.png",
		}

		if (status === null) {
			resultOutput.textContent = "Error Occured!";
			return;
		}
		if (status >= 400) {
			resultOutput.textContent = error_data.error;;
			return;
		}

		const divContainer = document.createElement("div");
		divContainer.classList.add("d-flex", "gap-3", "align-items-center");

		const userImgContainer = document.createElement("img");
		userImgContainer.style.width = "50px";  // 幅を指定
		userImgContainer.style.height = "50px"; // 高さを指定
		userImgContainer.style.objectFit = "cover";  // 画像の縦横比を保つための設定
		userImgContainer.style.borderRadius = "50%";  // 画像を丸くする
		userImgContainer.src = data.avatarPath;
		const usernameContainer = document.createElement("div");
		usernameContainer.classList.add("text-dark", "fs-5");
		usernameContainer.textContent = data.username;

		divContainer.appendChild(userImgContainer);
		divContainer.appendChild(usernameContainer);
		resultOutput.appendChild(divContainer);

		const addButton = document.createElement("button");
		addButton.classList.add("btn", "btn-primary", "btn-lg");
		addButton.textContent = "add";
		addButton.type = "button";
		addButton.addEventListener("click", () => {
			// ここにaddボタンが押された時の処理を書く
			console.log("Add button clicked!");
			addButton.classList.remove("btn-primary");
			addButton.classList.add("btn-secondary");
		});
		resultOutput.appendChild(addButton);
	})
	
}