export default function GameResult() {
  const message = {
    win: "YOU WIN",
    lose: "YOU LOSE",
  };
  return `
    <div class="game-result-container text-center vh-100">
      <div class="wl-container my-5">
        <h1 class="game-win-lose wl-first">YOU WIN</h1>
        <h1 class="game-win-lose wl-second">YOU WIN</h1>
        <h1 class="game-win-lose wl-third">YOU WIN</h1>
      </div>
      <div class="game-result d-flex justify-content-between w-100 mb-5 py-1">
        <div class="w-50 text-end game-result-left-player-bgc px-5">12</div>
        <div class="w-50 text-start game-result-right-player-bgc px-5">0</div>
      </div>
      <button type="button" class="my-5 py-3 px-5 game-result-button">Back To Home</button>
    </div>
  `;
}
