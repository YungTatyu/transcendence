import SPA from "../spa.js";

export default function GameResult(params) {
  if (!params) {
    return SPA.navigate("/", null, true);
  }
  const message = params.win ? "YOU WIN" : "YOU LOSE";
  return `
    <div class="game-result-container text-center vh-100">
      <div class="wl-container my-5">
        <h1 class="game-win-lose wl-first">${message}</h1>
        <h1 class="game-win-lose wl-second">${message}</h1>
        <h1 class="game-win-lose wl-third">${message}</h1>
      </div>
      <div class="game-result d-flex justify-content-between w-100 mb-5 py-1">
        <div class="w-50 text-end game-result-left-player-bgc px-5">${params.left}</div>
        <div class="w-50 text-start game-result-right-player-bgc px-5">${params.right}</div>
      </div>
      <button type="button" class="my-5 py-3 px-5 game-result-button">Back To Home</button>
    </div>
  `;
}

export function setupGameResult() {
  const homeButtonEle = document.querySelector(".game-result-button");
  homeButtonEle.addEventListener("click", (event) => {
    event.preventDefault();
    SPA.navigate("/", null, true);
  })
}
