import TitileAndHomeButton from "../components/titleAndHomeButton.js";

function UserInfo(className, text) {
  return `
    <div class="${className}">
      <p class="user-profile-text me-2">${text}</p>
      <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
    </div>
      `;
}

function UserMatchHistory(idName, text1, text2, text3) {
  return `
   <div id="${idName} " class="row row-cols-3">
        <div class="col">${text1}</div>
        <div class="col">${text2}</div>
        <div class="col">${text3}</div>
      </div>
      `;
}

export default function Profile() {
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
      ${UserMatchHistory("row-data", "10", "5", "3")}
      ${UserMatchHistory("row-label", "Wins", "Losses", "Tournament Wins")}
    </div>

    <div class="d-grid gap-2 col-4 mx-auto mt-5">
      <button class="match-history-button btn btn-primary rounded-pill" type="button">Match History</button>
    </div>

    `;
}
