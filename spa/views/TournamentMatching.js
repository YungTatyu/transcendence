import MatchingRoom, { renderMatchingRoom } from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import WaitOrStart from "../components/WaitOrStart.js";

export default function TournamentMatching() {
	return `
      ${TitleMatchingRoom("Tournament")}
      ${tournamentMatchingInfo()}
      ${MatchingRoom()}
      ${WaitOrStart()}
	`;
}

export function setupTournamentMatching() {
	let jsonData = [
		{ avatarPath: "/assets/user.png", name: "rikeda1" },
		{ avatarPath: "/assets/user.png", name: "rikeda2" },
		{ avatarPath: "/assets/user.png", name: "rikeda3" },
		{ avatarPath: "/assets/user.png", name: "rikeda4" },
	];

	renderMatchingRoom(jsonData);
	changeMatchingInfo(4, 16, 9);
}

function tournamentMatchingInfo() {
	return `
      <div id="tournament-matching-info" class="d-flex flex-column justify-content-center align-items-center text-center">
        <span>
          <span id="current-players">3</span>/<span id="max-players">16</span> players
        </span>
        <span>
          start in <span id="matching-remain-sec">[59]</span> sec
        </span>
      </div>
    `;
}

function changeMatchingInfo(playerSize, maxPlayerSize, remainSec) {
	const currentPlayers = document.getElementById("current-players");
	const maxPlayers = document.getElementById("max-players");
	const matchingRemainSec = document.getElementById("matching-remain-sec");

	currentPlayers.textContent = playerSize;
	maxPlayers.textContent = maxPlayerSize;
	matchingRemainSec.textContent = `[${remainSec}]`;
}
