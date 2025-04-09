export default function TournamentInfo() {
  return `
    <div class="match-vs d-flex justify-content-between w-100 mb-5 py-1 mt-5">
      <div class="w-50 text-center match-left-player px-5"></div>
      <div class="d-flex justify-content-center align-items-center">
        <div class="diamond px-5 position-absolute bg-white d-flex justify-content-center align-items-center">
          <span class="diamond-text text-black text-center fw-bold">VS</span>
        </div>
      </div>
      <div class="w-50 text-center match-right-player px-5"></div>
    </div>
	`;
}

export function renderPlayers(leftPlayerName, rightPlayerName) {
  const leftPlayer = document.querySelector(".match-left-player");
  const rightPlayer = document.querySelector(".match-right-player");

  leftPlayer.textContent = leftPlayerName;
  rightPlayer.textContent = rightPlayerName;
}
