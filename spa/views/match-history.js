import stateManager from "../stateManager.js";

export default function MatchHistory() {
  return `

    <div class="container text-center">
      <div class="row">
        <div class="col align-self-start">
          <p class="title text-start">MATCH HISTORY</p>
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

    <div class="container text-center history-container">
      <div class="row row-cols-5 header-row">
        <div class="col">MODE</div>
        <div class="col">PLAYER</div>
        <div class="col">RESULT</div>
        <div class="col">SCORE</div>
        <div class="col">DATE</div>
      </div>

      <div id="content-row"">
      <!-- ここにAPIから取得したデータが挿入される -->
        <div class="row row-cols-5 mt-2">
          <div class="col">Quick Play</div>
          <div class="col text-center">
            <img src="./assets/42.png" alt="ロゴ" class="square-img rounded-circle me-2" >
            <span>username</span>
          </div>
          <div class="col">WIN</div>
          <div class="col">11-3</div>
          <div class="col">2025/01/01</div>
        </div>
        <!-- ここまでAPIから取得したデータが挿入される -->
      </div>
    </div>  

  `;
}

// APIからデータを取得して `.content-row` に挿入
async function fetchMatchHistory() {
  try {
    // TODO: jwtからユーザーIDを取得

    // match historyを取得（apiを適切なものに変更する）
    const response = await fetch("https://api.example.com/matches/histories/<userId>");
    const data = await response.json();

    // データを表示するコンテナを取得
    const container = document.getElementById("content-row");

    // データが空の場合
    if (!data.results || data.results.length === 0) {
      container.innerHTML = "<p>試合履歴がありません</p>";
      return;
    }
   
    // 対戦相手のavatar_pathとusernameを取得
    // opponentId のリストを作成 
    const opponentIds = [...new Set(data.results.map(match => match.opponents[0].id))];

    // すべての opponentId のユーザーデータを取得 (idごとにfetchを実行)
     const userResponses = await Promise.all(
      opponentIds.map(id => fetch(`https://api.example.com/users/${id}`).then(res => res.json()))
    );

    // id をキーとして avatar_path と username を格納する
    const userProfiles = {};
    userResponses.forEach(user => {
      userProfiles[user.id] = {
        avatar: user.avatar_path,
        username: user.username
      };
    });


    // データをループしてHTMLを作成
    let contentHTML = "";
    data.results.forEach(match => {
      // 対戦相手のデータを取得
      const opponent = match.opponents[0];
      const opponentData= userProfiles[opponent.id];
      // 試合結果により色を変更
      const resultClass = match.result.toUpperCase() === "WIN" ? "text-primary" : "text-danger";


      contentHTML += `
        <div class="row row-cols-5 mt-2">
          <div class="col">${match.mode}</div>
          <div class="col text-center">
            <img src="${opponentData.avatar}" alt="Player" class="square-img rounded-circle me-2" width="40">
            <span>${opponentData.username}</span>
          </div>
          <div class="col ${resultClass}">${match.result.toUpperCase()}</div>
          <div class="col">${match.userScore} - ${match.opponents.score}</div>
          <div class="col">${match.date}</div>
        </div>
      `;
    });

    // HTMLを挿入
    container.innerHTML = contentHTML;

  } catch (error) {
    console.error("マッチ履歴の取得に失敗しました", error);
  }
}

// ページロード後にデータを取得
window.onload = fetchMatchHistory;
