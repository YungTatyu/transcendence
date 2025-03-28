import MatchingRoom, {
  renderMatchingRoom,
} from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import WaitOrStart from "../components/WaitOrStart.js";

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
  function changeMatchingInfo() {
    const matchingInfo = document.getElementById("matching-info");

    matchingInfo.innerHTML = "OPPONENT FOUND.";
    matchingInfo.style.color = "#0CC0DF";
  }

  const jsonData = [{ avatarPath: "/assets/user.png", name: "rikeda" }];

  renderMatchingRoom(jsonData);
}
