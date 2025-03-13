import TitileAndHomeButton from "../components/titleAndHomeButton.js";

export function MatchHistoryData(
  mode,
  playerAvatar,
  playerName,
  result,
  score,
  date,
) {
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

export default function MatchHistory() {
  return `

    ${TitileAndHomeButton("MATCH HISTORY")}

    <div class="container text-center history-container">
      <div class="row row-cols-5 header-row">
        <div class="col">MODE</div>
        <div class="col">PLAYER</div>
        <div class="col">RESULT</div>
        <div class="col">SCORE</div>
        <div class="col">DATE</div>
      </div>

      <div id="content-row"">
        ${MatchHistoryData("1v1", "./assets/42.png", "Player1", "Win", "10-5", "2021-10-10")}
      </div>
    </div>  

  `;
}
