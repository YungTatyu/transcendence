import MatchingRoom, {
  renderMatchingRoom,
} from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import NeonInfo, { renderNeonInfo } from "../components/NeonInfo.js";
import TournamentMatchingInfo from "../services/tournament/TournamentMatchingInfo.js";
import WsTournamentMatchingManager from "../services/tournament/WsTournamentMatchingManager.js";

export default function TournamentMatching() {
  return `
      ${TitleMatchingRoom("TOURNAMENT")}
      ${TournamentMatchingInfo()}
      ${MatchingRoom()}
      ${NeonInfo()}
	`;
}

export function setupTournamentMatching() {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!accessToken) {
      SPA.navigate("/");
      return;
    }
    renderMatchingRoom([]);
    renderNeonInfo("Wait...", "#0ca5bf");
    WsTournamentMatchingManager.connect(accessToken);
  } catch (error) {
    console.error(error);
  }
}

export function cleanupTournamentMatching() {
  WsTournamentMatchingManager.disconnect();
}
