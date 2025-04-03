import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
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
          <div id="wins" class="col">loading...</div>
          <div id="losses" class="col">loading...</div>
          <div id="tournament-wins" class="col">loading...</div>
      </div>
      <div id="row-label " class="row row-cols-3">
          <div class="col">Wins game</div>
          <div class="col">Losses game</div>
          <div class="col">Tournament wins</div>
      </div>
        `;
  }

  return `

    ${TitleAndHomeButton("PROFILE")}
    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img src="${config.userService}/media/images/default/default.png" class="square-img-user-avatar rounded-circle me-2 js-user-avatar" >
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

function getobjs(){
  const changeAvatarButton = document.querySelector(".js-pen-avatar");
  const changeUnameButton = document.querySelector(".js-pen-username");
  const changePasswordButton = document.querySelector(".js-pen-password");
  const changeMailButton = document.querySelector(".js-pen-mail");
  const matchHistoryButton = document.querySelector(".js-match-history-button");

  return {
    changeAvatarBtn: {
      btn: changeAvatarButton,
      handle: () => SPA.navigate("/profile/avatar")
    },
    changeUnameBtn: {
      btn: changeUnameButton,
      handle: () => SPA.navigate("/profile/username")
    },
    changePassBtn: {
      btn: changePasswordButton,
      handle: () => SPA.navigate("/profile/password")
    },
    changeMailBtn: {
      btn: changeMailButton,
      handle: () => SPA.navigate("/profile/mail")
    },
    matchHistoryBtn: {
      btn: matchHistoryButton,
      handle: () => SPA.navigate("/history/match")
    }
  }
}


export async function setupProfile() {
  // const changeAvatarButton = document.querySelector(".js-pen-avatar");
  // const toChangeAvatar = () => SPA.navigate("/profile/avatar");
  // changeAvatarButton.addEventListener("click", toChangeAvatar);

  // const changeUsernameButton = document.querySelector(".js-pen-username");
  // const toChangeUsername = () => SPA.navigate("/profile/username");
  // changeUsernameButton.addEventListener("click", toChangeUsername);

  // const changePasswordButton = document.querySelector(".js-pen-password");
  // const tochnagePassword = () => SPA.navigate("/profile/password");
  // changePasswordButton.addEventListener("click", tochnagePassword);

  // const changeMailButton = document.querySelector(".js-pen-mail");
  // const toChangeMail = () => SPA.navigate("/profile/mail");
  // changeMailButton.addEventListener("click", toChangeMail);

  // const matchHistoryButton = document.querySelector(".js-match-history-button");
  // const toMatchHistory = () => SPA.navigate("/history/match");
  // matchHistoryButton.addEventListener("click", toMatchHistory);
  const btns = getobjs();
  btns.changeAvatarBtn.btn.addEventListener("click", btns.changeAvatarBtn.handle);
  btns.changeUnameBtn.btn.addEventListener("click", btns.changeUnameBtn.handle);
  btns.changePassBtn.btn.addEventListener("click", btns.changePassBtn.handle);
  btns.changeMailBtn.btn.addEventListener("click", btns.changeMailBtn.handle);
  btns.matchHistoryBtn.btn.addEventListener("click", btns.matchHistoryBtn.handle);

  if (stateManager.state.username && stateManager.state.avatarUrl) {
    document.querySelector(".js-username").textContent =
      stateManager.state.username;
    document.querySelector(".js-user-avatar").src =
      stateManager.state.avatarUrl;
    return;
  }

  const { status: uStatus, data: uData } = await fetchApiNoBody(
    "GET",
    config.userService,
    `/users?userid=${stateManager.state.userId}`,
  );

  if (uStatus === null || uStatus >= 400) {
    console.error("ユーザー情報の取得に失敗しました");
    return;
  }
  const avatarUrl = `${config.userService}${uData.avatarPath}`;

  document.querySelector(".js-username").textContent = uData.username;
  document.querySelector(".js-user-avatar").src = avatarUrl;

  stateManager.setState({ username: uData.username });
  stateManager.setState({ avatarUrl: avatarUrl });

  if (!stateManager.state.userId) {
    return;
  }
  const { status, data } = await fetchApiNoBody(
    "GET",
    config.matchService,
    `/matches/statistics/${stateManager.state.userId}`,
  );

  if (status === null || status >= 400) {
    console.error("試合統計情報の取得に失敗しました");
    return;
  }
  const wins = document.getElementById("wins");
  const losses = document.getElementById("losses");
  const tournamentWins = document.getElementById("tournament-wins");

  wins.textContent = data.matchWinCount;
  losses.textContent = data.matchLoseCount;
  tournamentWins.textContent = data.tournamentWinnerCount;

}

export function cleanupProfile() {
  console.log("[cleanupProfile] called");

  const btns = getobjs();
  btns.changeAvatarBtn.btn.removeEventListener("click", btns.changeAvatarBtn.handle);
  btns.changeUnameBtn.btn.removeEventListener("click", btns.changeUnameBtn.handle);
  btns.changePassBtn.btn.removeEventListener("click", btns.changePassBtn.handle);
  btns.changeMailBtn.btn.removeEventListener("click", btns.changeMailBtn.handle);
  btns.matchHistoryBtn.btn.removeEventListener("click", btns.matchHistoryBtn.handle);
}