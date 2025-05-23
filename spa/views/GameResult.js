import SPA from "../spa.js";
import stateManager from "../stateManager.js";

export default function GameResult(params) {
  const expectedKeys = ["left", "right", "win"];
  if (
    !params ||
    !expectedKeys.every((key) => key in params && params[key] !== undefined)
  ) {
    stateManager.setState({ tournamentId: null });
    return `
      <div class="game-result-container text-center vh-100">
        <button type="button" class="my-5 py-3 px-5 game-result-button">Back To Home</button>
      </div>
    `;
  }
  const message = params.win ? "YOU WIN" : "YOU LOSE";
  return `
    <div class="game-result-container text-center vh-100">
      <div class="wl-container my-5">
        <h1 class="game-win-lose">${message}</h1>
      </div>
      <div class="game-result d-flex justify-content-between w-100 mb-5 py-1">
        <div class="w-50 text-end game-result-left-player-bgc px-5">${params.left}</div>
        <div class="w-50 text-start game-result-right-player-bgc px-5">${params.right}</div>
      </div>
      <button type="button" class="my-5 py-3 px-5 game-result-button">Back To Home</button>
    </div>
  `;
}

export async function setupGameResult() {
  // stateにtournamentIdがあればTournamentへ、なければHomeへ
  let route = "/home";

  if (stateManager.state.tournamentId) {
    route = "/tournament";
    const button = document.querySelector(".game-result-button");
    if (!button) {
      return;
    }
    button.textContent = "Back To Tournament";
  }
  document
    .querySelector(".game-result-button")
    ?.addEventListener("click", (event) => {
      event.preventDefault();
      SPA.navigate(route, null, true);
    });
}
