import MatchingRoom, { renderMatchingRoom } from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";

export default function QuickPlayMatching() {
	return TitleMatchingRoom("Quick Play") + MatchingRoom();
}

export function setupQuickPlayMatching() {
	let jsonData = [{ avatarPath: "/asserts/user.png", name: "rikeda" }];

	renderMatchingRoom(jsonData);
}
