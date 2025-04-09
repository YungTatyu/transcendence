import WaitOrStart, { renderWaitOrStart } from "../components/WaitOrStart.js";
import WsTournamentManager from "../services/tournament/WsTournamentManager.js";
import stateManager from "../stateManager.js";

export default function Tournament() {
  return `
    <div class="match-vs d-flex justify-content-between w-100 mb-5 py-1 mt-5">
      <div class="w-50 text-center match-left-player px-5">rikeda1</div>
      <div class="d-flex justify-content-center align-items-center">
        <div class="diamond px-5 position-absolute bg-white d-flex justify-content-center align-items-center">
          <span class="diamond-text text-black text-center fw-bold">VS</span>
        </div>
      </div>
      <div class="w-50 text-center match-right-player px-5">rikeda2</div>
    </div>
    ${TournamentBracket()}
    ${WaitOrStart()}
  `;
}

export function setupTournament() {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    const tournamentId = stateManager.state.tournamentId;
    if (!(accessToken && tournamentId)) {
      SPA.navigate("/home");
      return;
    }
    renderWaitOrStart("WAIT...", "#0ca5bf");
    WsTournamentManager.connect(accessToken, tournamentId);
  } catch (error) {
    console.error(error);
  }
}

export function cleanupTournament() {
  WsTournamentManager.disconnect();
}
