import TitileAndHomeButton from "../components/titleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function Profile() {
  function UserInfo(className, textClass, text, penClass) {
    return `
      <div class="${className}">
        <p class="user-profile-text me-2 ${textClass}">${text}</p>
        <img src="/assets/pencil.png" class="pencil-icon align-self-start mt-n1 ${penClass}">
      </div>
        `;
  }

  function UserMatchHistory(idName) {
    //Loadingの部分はAPIから取得した値で上書きする
    return `
      <div id="row-data " class="row row-cols-3">
          <div class="col">loading...</div>
          <div class="col">loading...</div>
          <div class="col">loading...</div>
      </div>
      <div id="row-label " class="row row-cols-3">
          <div class="col">Wins</div>
          <div class="col">Losses</div>
          <div class="col">Tournament Wins</div>
      </div>
        `;
  }

  return `

    ${TitileAndHomeButton("PROFILE")}
    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img src="/assets/42.png" class="square-img-user-avatar rounded-circle me-2 js-user-avatar" >
          <img src="/assets/pencil.png" class="pencil-icon align-self-start mt-n1 js-pen-avatar">
      </div>

      ${UserInfo("d-inline-flex align-items-center mt-5", "js-username", "UserName", "js-pen-username")}
      ${UserInfo("d-inline-flex align-items-center", "js-password", "Password", "js-pen-password")}
      ${UserInfo("d-inline-flex align-items-center", "js-mail", "Mail", "js-pen-mail")}

     
    </div>

    <div class="container text-center mt-4 match-record">
      ${UserMatchHistory()}
    </div>

    <div class="d-grid gap-2 col-4 mx-auto mt-5">
      <button class="match-history-button btn btn-primary rounded-pill js-match-history-button" type="button">Match History</button>
    </div>

    `;
}

export async function setupProfile() {
  const changeAvatarButton = document.querySelector(".js-pen-avatar");
  changeAvatarButton.addEventListener("click", () => {
    SPA.navigate("/profile/avatar");
  });

  const changeUsernameButton = document.querySelector(".js-pen-username");
  changeUsernameButton.addEventListener("click", () => {
    SPA.navigate("/profile/username");
  });

  const changePasswordButton = document.querySelector(".js-pen-password");
  changePasswordButton.addEventListener("click", () => {
    SPA.navigate("/profile/password");
  });

  const changeMailButton = document.querySelector(".js-pen-mail");
  changeMailButton.addEventListener("click", () => {
    SPA.navigate("/profile/mail");
  });

  const matchHistoryButton = document.querySelector(".js-match-history-button");
  matchHistoryButton.addEventListener("click", () => {
    SPA.navigate("/history/match");
  });

  if (stateManager.state.username && stateManager.state.avatar_path) {
    document.querySelector(".js-username").textContent =
      stateManager.state.username;
    document.querySelector(".js-user-avatar").src =
      stateManager.state.avatar_path;
    return;
  }

  const response = await fetch(
    `${config.userService}/users?userid=${stateManager.state.userId}`,
  );
  const status = response.status;
  const data = await response.json();

  if (status === null) {
    errorOutput.textContent = "Error Occured!";
    return;
  }
  if (status >= 400) {
    errorOutput.textContent = JSON.stringify(data.error, null, "\n");
    return;
  }
  document.querySelector(".js-username").textContent = data.username;
  document.querySelector(".js-user-avatar").src = data.avatar_path;

  stateManager.setState({ username: data.username });
  stateManager.setState({ avatarPath: data.avatar_path });
}
