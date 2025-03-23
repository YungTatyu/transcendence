import TitileAndHomeButton from "../components/titleAndHomeButton.js";

export default function MatchHistory() {
  function MatchHistoryData() {
    const playerAvatar = "/assets/user.png";
    //APIから取得した値で上書する
    return `
      <div class="row row-cols-5 mt-2">
        <div class="col">loading...</div>
        <div class="col text-center">
          <img src="${playerAvatar}" alt="ロゴ" class="square-img rounded-circle me-2" >
          <span>loading...</span>
        </div>
        <div class="col">loading...</div>
        <div class="col">loading...</div>
        <div class="col">loading...</div>
      </div>
      `;
  }
  return `

    ${TitileAndHomeButton("MATCH HISTORY")}

    <div class="container text-center match-history-container">
      <div class="row row-cols-5 match-history-table-header">
        <div class="col">MODE</div>
        <div class="col">PLAYER</div>
        <div class="col">RESULT</div>
        <div class="col">SCORE</div>
        <div class="col">DATE</div>
      </div>

      <div id="match-history-table"">
        ${MatchHistoryData()}
      </div>
    </div>  

  `;
}
