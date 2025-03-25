import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitileAndHomeButton from "../components/titleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function Profile() {
  function UserInfo(className, text) {
    return `
      <div class="${className}">
        <p class="user-profile-text me-2">${text}</p>
        <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
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

    ${TitileAndHomeButton("PROFILE")}
    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img id="user-avatar" src="/assets/user.png" class="square-img-user-avatar rounded-circle me-2 pencil-icon" >
          <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>

      ${UserInfo("d-inline-flex align-items-center mt-5", "UserName")}
      ${UserInfo("d-inline-flex align-items-center", "Password")}
      ${UserInfo("d-inline-flex align-items-center", "Mail")}

     
    </div>

    <div class="container text-center mt-4 match-record">
      ${UserMatchHistory()}
    </div>

    <div class="d-grid gap-2 col-4 mx-auto mt-5">
      <button class="match-history-button btn btn-primary rounded-pill" type="button">Match History</button>
    </div>

    `;
}

export async function setupProfile() {
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
