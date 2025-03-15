import TitileAndHomeButton from "../components/titleAndHomeButton.js";

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
    //APIから取得する
    const wins = "5";
    const losses = "1";
    const tWins = "1";

    return `
      <div id="row-data " class="row row-cols-3">
          <div class="col">${wins}</div>
          <div class="col">${losses}</div>
          <div class="col">${tWins}</div>
      </div>
      <div id="row-label " class="row row-cols-3">
          <div class="col">"Wins"</div>
          <div class="col">"Losses"</div>
          <div class="col">"Tournament Wins"</div>
      </div>
        `;
  }

  return `

    ${TitileAndHomeButton("PROFILE")}
    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img id="user-avatar" src="./assets/42.png" alt="ロゴ" class="square-img-user-avatar rounded-circle me-2 pencil-icon" >
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
