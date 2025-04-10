import NeonInfo, { renderNeonInfo } from "../components/NeonInfo.js";
import WsTournamentManager from "../services/tournament/WsTournamentManager.js";
import stateManager from "../stateManager.js";
import TournamentBracket from "../services/tournament/TournamentBracket.js";
import TournamentInfo from "../services/tournament/TournamentInfo.js";

export default function Tournament() {
	return `
    ${TournamentInfo()}
    ${TournamentBracket()}
    ${NeonInfo()}
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
    renderNeonInfo("WAIT...", "#0ca5bf");

    // INFO WebSocket接続時、WebSocketからのデータの有無に関わらず、必ず描画を行う
    WsTournamentManager.connect(accessToken, tournamentId);
    WsTournamentManager.setCanRender(true);
    WsTournamentManager.forceRenderTournament();
  } catch (error) {
    console.error(error);
  }
}

export function cleanupTournament() {
  // INFO 別画面に遷移する場合、Connectionは維持し、描画はさせない
  WsTournamentManager.setCanRender(false);
}
