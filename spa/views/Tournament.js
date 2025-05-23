import NeonInfo, { renderNeonInfo } from "../components/NeonInfo.js";
import TournamentBracket from "../services/tournament/TournamentBracket.js";
import TournamentInfo from "../services/tournament/TournamentInfo.js";
import WsTournamentManager from "../services/tournament/WsTournamentManager.js";
import stateManager from "../stateManager.js";

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
      SPA.navigate("/home");
      return;
    }
    renderNeonInfo("WAIT...", "#0ca5bf");

    WsTournamentManager.setCanRender(true);
    // INFO socketを作成していない場合のみ作成
    if (WsTournamentManager.socket === null) {
      WsTournamentManager.connect(accessToken, tournamentId);
    } else {
      WsTournamentManager.forceRenderTournament();
    }
  } catch (error) {
    console.error(error);
  }
}

export function cleanupTournament() {
  // INFO 別画面に遷移する場合、Connectionは維持し、描画はさせない
  WsTournamentManager.setCanRender(false);
}
