export default function TournamentMatchingInfo() {
  return `
    <div id="tournament-matching-info" class="d-flex flex-column justify-content-center align-items-center text-center">
      <span>
        <span id="current-players"></span>/<span id="max-players"></span> players
      </span>
      <span>
        start in <span id="matching-remain-sec"></span> sec
      </span>
    </div>
  `;
}

export function renderMatchingInfo(playerSize, maxPlayerSize) {
  const currentPlayers = document.getElementById("current-players");
  const maxPlayers = document.getElementById("max-players");

  currentPlayers.textContent = playerSize;
  maxPlayers.textContent = maxPlayerSize;
}

export function renderTimer(endTime) {
  const matchingRemainSec = document.getElementById("matching-remain-sec");
  matchingRemainSec.textContent = `[${endTime}]`;
}
