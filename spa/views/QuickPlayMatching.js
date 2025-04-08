import MatchingRoom, {
  renderMatchingRoom,
} from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import WaitOrStart, { renderWaitOrStart } from "../components/WaitOrStart.js";
import MatchingInfo, {
  renderMatchingInfo,
} from "../services/match/MatchingInfo.js";
import WsQuickPlayMatchingManager from "../services/match/WsQuickPlayMatchingManager.js";

export default function QuickPlayMatching() {
  return `
      ${TitleMatchingRoom("QUICK PLAY")}
      ${MatchingInfo()}
      ${MatchingRoom()}
      ${WaitOrStart()}
  `;
}

export function setupQuickPlayMatching() {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!accessToken) {
      SPA.navigate("/");
      return;
    }
    renderMatchingRoom([]);
    renderWaitOrStart("WAIT...", "#0CC0DF");
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
