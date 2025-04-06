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

export function renderMatchingInfo(playerSize, maxPlayerSize, remainSec) {
  const currentPlayers = document.getElementById("current-players");
  const maxPlayers = document.getElementById("max-players");
  const matchingRemainSec = document.getElementById("matching-remain-sec");

  currentPlayers.textContent = playerSize;
  maxPlayers.textContent = maxPlayerSize;
  matchingRemainSec.textContent = `[${remainSec}]`;
}
