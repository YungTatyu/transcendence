import MatchingRoom, { renderMatchingRoom } from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";

export default function QuickPlayMatching() {
	return `
      ${TitleMatchingRoom("Quick Play")}
      <p id="matching-info" class="d-flex justify-content-center align-items-center">
        LOOKING FOR AN OPPONENT.
      </p>
      ${MatchingRoom()}
	`;
}

export function setupQuickPlayMatching() {
	let jsonData = [{ avatarPath: "/assets/user.png", name: "rikeda" }];

	renderMatchingRoom(jsonData);
}
