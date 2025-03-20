import MatchingRoom, { renderMatchingRoom } from "../components/MatchingRoom.js";

export default function QuickPlayMatching() {
	return MatchingRoom();
}

export function setupQuickPlayMatching() {
	let jsonData = [{ avatarPath: "/asserts/user.png", name: "rikeda" }];

	renderMatchingRoom(jsonData);
}
