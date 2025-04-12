import MatchingRoom, {
  renderMatchingRoom,
} from "../components/MatchingRoom.js";
import NeonInfo, { renderNeonInfo } from "../components/NeonInfo.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import MatchingInfo, {
  renderMatchingInfo,
} from "../services/match/MatchingInfo.js";
import WsQuickPlayMatchingManager from "../services/match/WsQuickPlayMatchingManager.js";

export default function QuickPlayMatching() {
  return `
      ${TitleMatchingRoom("QUICK PLAY")}
      ${MatchingInfo()}
      ${MatchingRoom()}
      ${NeonInfo()}
  `;
}

export function setupQuickPlayMatching() {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!accessToken) {
      SPA.navigate("/home");
      return;
    }
    renderMatchingRoom([]);
    renderNeonInfo("WAIT...", "#0CC0DF");
    renderMatchingInfo("LOOKING FOR AN OPPONENT.", "#7733ff");
    WsQuickPlayMatchingManager.connect(accessToken);
  } catch (error) {
    console.error(error);
    renderMatchingInfo("faild quickplay matching.", "#FF0000");
  }
}

export function cleanupQuickPlayMatching() {
  WsQuickPlayMatchingManager.disconnect();
}
