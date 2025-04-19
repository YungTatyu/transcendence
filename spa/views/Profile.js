import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

const handleChAvatar = () => SPA.navigate("/profile/avatar");
const handleChUname = () => SPA.navigate("/profile/username");
const handleChPassword = () => SPA.navigate("/profile/password");
const handleChMail = () => SPA.navigate("/profile/mail");
const handleMatchHistory = () => SPA.navigate("/history/match");

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
    return `
      <div id="row-data " class="row row-cols-3">
          <div id="wins" class="col">loading...</div>
          <div id="losses" class="col">loading...</div>
          <div id="tournament-wins" class="col">loading...</div>
      </div>
      <div id="row-label " class="row row-cols-3">
          <div class="col">Wins</div>
          <div class="col">Losses</div>
          <div class="col">Tournament Wins</div>
      </div>
        `;
  }

  return `

    ${TitleAndHomeButton("PROFILE")}
    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img src="${config.userService}/media/images/default/default_image.png" class="square-img-user-avatar rounded-circle me-2 js-user-avatar" >
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

function getElements() {
  const changeAvatarBtn = document.querySelector(".js-pen-avatar");
  const changeUnameBtn = document.querySelector(".js-pen-username");
  const changePasswordBtn = document.querySelector(".js-pen-password");
  const changeMailBtn = document.querySelector(".js-pen-mail");
  const matchHistoryBtn = document.querySelector(".js-match-history-button");

  if (
    !(
      changeAvatarBtn &&
      changeUnameBtn &&
      changePasswordBtn &&
      changeMailBtn &&
      matchHistoryBtn
    )
  ) {
    return null;
  }

  return [
    { btn: changeAvatarBtn, handle: handleChAvatar },
    { btn: changeUnameBtn, handle: handleChUname },
    { btn: changePasswordBtn, handle: handleChPassword },
    { btn: changeMailBtn, handle: handleChMail },
    { btn: matchHistoryBtn, handle: handleMatchHistory },
  ];
}

export async function setupProfile() {
  const elements = getElements();
  if (!elements) {
    return;
  }
  for (const { btn, handle } of elements) {
    btn.addEventListener("click", handle);
  }

  if (stateManager.state.username && stateManager.state.avatarUrl) {
    const jsUsername = document.querySelector(".js-username");
    const jsUserAvatar = document.querySelector(".js-user-avatar");
    if (!(jsUsername && jsUserAvatar)) {
      return;
    }
    jsUsername.textContent = stateManager.state.username;
    jsUserAvatar.src = stateManager.state.avatarUrl;
  } else {
    const { status: uStatus, data: uData } = await fetchApiNoBody(
      "GET",
      config.userService,
      `/users?userid=${stateManager.state.userId}`,
    );

    if (uStatus === null || uStatus >= 400) {
      console.error("ユーザー情報の取得に失敗しました");
    } else {
      const avatarUrl = `${config.userService}${uData.avatarPath}`;

      const jsUsername = document.querySelector(".js-username");
      const jsUserAvatar = document.querySelector(".js-user-avatar");
      if (!(jsUsername && jsUserAvatar)) {
        return;
      }
      jsUsername.textContent = uData.username;
      jsUserAvatar.src = avatarUrl;

      stateManager.setState({ username: uData.username });
      stateManager.setState({ avatarUrl: avatarUrl });
    }
  }

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

  if (!(wins && losses && tournamentWins)) {
    return;
  }
  wins.textContent = data.matchWinCount;
  losses.textContent = data.matchLoseCount;
  tournamentWins.textContent = data.tournamentWinnerCount;
}

export function cleanupProfile() {
  for (const { btn, handle } of getElements()) {
    btn.removeEventListener("click", handle);
  }
}
