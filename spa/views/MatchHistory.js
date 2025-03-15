import TitileAndHomeButton from "../components/titleAndHomeButton.js";

export default function MatchHistory() {
  function MatchHistoryData() {
    const mode = "QuickPlay";
    const playerAvatar = "/assets/42.png";
    const playerName = "playerA";
    const result = "WIN";
    const score = "1-11";
    const date = "2025/01/01";

    return `
      <div class="row row-cols-5 mt-2">
        <div class="col">${mode} </div>
        <div class="col text-center">
          <img src="${playerAvatar}" alt="ロゴ" class="square-img rounded-circle me-2" >
          <span>${playerName} </span>
        </div>
        <div class="col">${result}</div>
        <div class="col">${score}</div>
        <div class="col">${date}</div>
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
