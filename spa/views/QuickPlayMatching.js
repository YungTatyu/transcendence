import MatchingRoom, {
  renderMatchingRoom,
} from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import WaitOrStart, { renderWaitOrStart } from "../components/WaitOrStart.js";
import stateManager from "../stateManager.js";
import WsQuickPlayMatchingManager from "../services/match/WsQuickPlayMatchingManager.js";

export default function QuickPlayMatching() {
  function matchingInfo() {
    return `
      <p id="matching-info" class="d-flex justify-content-center align-items-center">
        LOOKING FOR AN OPPONENT.
      </p>
    `;
  }

  return `
      ${TitleMatchingRoom("QUICK PLAY")}
      ${matchingInfo()}
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
    WsQuickPlayMatchingManager.connect(accessToken);
  } catch (error) {
    console.err(error);
  }

  // const jsonData = [{ avatarPath: "/assets/user.png", name: "rikeda" }];

  // renderMatchingRoom(jsonData);
  renderWaitOrStart("START", "#ffffff");
}

function changeMatchingInfo() {
  const matchingInfo = document.getElementById("matching-info");

  matchingInfo.innerHTML = "OPPONENT FOUND.";
  matchingInfo.style.color = "#0CC0DF";
}
