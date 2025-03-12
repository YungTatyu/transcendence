import stateManager from "../stateManager.js";

export default function Profile() {
  return `

    <div class="container text-center">
      <div class="row">
        <div class="col align-self-start">
          <p class="title text-start">PROFILE</p>
        </div>
        <div class="col align-self-end">
          <div class="position-relative">
            <svg class="home-icon bi bi-house-door-fill position-absolute top-0 end-0"
              xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor">
              <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img id="user-avatar" src="./assets/42.png" alt="ロゴ" class="square-img rounded-circle me-2" >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
              class="bi bi-pencil-fill align-self-start mt-n1"  viewBox="0 0 16 16">
              <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
          </svg>
      </div>


      <div class="d-inline-flex align-items-center mt-5">
          <p id="username" class="text me-2">UserName</p>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
              class="bi bi-pencil-fill align-self-start mt-n1"  viewBox="0 0 16 16">
              <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
          </svg>
      </div>


      <div class="d-inline-flex align-items-center">
          <p class="text me-2">Password</p>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
              class="bi bi-pencil-fill align-self-start mt-n1" viewBox="0 0 16 16">
              <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
          </svg>
      </div>

      <div class="d-inline-flex align-items-center">
          <p class="text me-2">Mail</p>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
              class="bi bi-pencil-fill align-self-start mt-n1"  viewBox="0 0 16 16">
              <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
          </svg>
      </div>
    </div>


    <div class="container text-center mt-4 match-record">
      <div id="row-content" class="row row-cols-3">
        <div class="col">Number1</div>
        <div class="col">Number2</div>
        <div class="col">Number3</div>
      </div>
      <div id="row-label" class="row row-cols-3">
        <div class="col">Wins</div>
        <div class="col">Losses</div>
        <div class="col">Tournament Wins</div>
      </div>
    </div>

    <div class="d-grid gap-2 col-6 mx-auto mt-5">
      <button class="btn btn-primary rounded-pill" type="button">Match History</button>
    </div>

  `;
}



// APIからデータを取得し、`#row-content` に挿入する関数
async function fetchProfileStats() {
  try {
    // TODO: 
    // jwtからuserIdを取得
    // 取得したuseridからusernameとavatar_pathを取得

    const user_response = await fetch("https://api.example.com/users/<userId>");
    const user_data = await user_response.json();

    document.getElementById("user-avatar").src = user_data.avatar_path
    document.getElementById("user-name").textContent = user_data.username;

    // APIのURL（適切なURLに変更）
    const match_response = await fetch("https://api.example.com/matches/statistics/<userId>");
    const match_data = await match_response.json();

    // データを表示するコンテナを取得
    const rowContent = document.getElementById("row-content");

    // 既存のデータをクリアし、新しいデータを挿入
    rowContent.innerHTML = `
      <div class="col">${match_data.matchWinCount}</div>
      <div class="col">${match_data.matchLoseCount}</div>
      <div class="col">${match_data.tournamentWinnerCount}</div>
    `;

  } catch (error) {
    console.error("プロフィールデータの取得に失敗しました", error);
  }
}

// ページがロードされたらデータを取得
window.onload = fetchProfileStats;

