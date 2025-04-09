import WaitOrStart, { renderWaitOrStart } from "../components/WaitOrStart.js";
import WsTournamentManager from "../services/tournament/WsTournamentManager.js";
import stateManager from "../stateManager.js";
import TournamentBracket from "../services/tournament/TournamentBracket.js";
import TournamentInfo from "../services/tournament/TournamentInfo.js";

export default function Tournament() {
  return `
    ${TournamentInfo()}
    ${TournamentBracket()}
    ${WaitOrStart()}
  `;
}

export function setupTournament() {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    const tournamentId = stateManager.state.tournamentId;
    if (!(accessToken && tournamentId)) {
      SPA.navigate("/");
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
