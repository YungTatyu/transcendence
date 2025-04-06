import MatchingRoom, {
  renderMatchingRoom,
} from "../components/MatchingRoom.js";
import TitleMatchingRoom from "../components/TitleMatchingRoom.js";
import WaitOrStart, { renderWaitOrStart } from "../components/WaitOrStart.js";
import TournamentMatchingInfo, {
  renderMatchingInfo,
} from "../services/tournament/TournamentMatchingInfo.js";

export default function TournamentMatching() {
  return `
      ${TitleMatchingRoom("TOURNAMENT")}
      ${TournamentMatchingInfo()}
      ${MatchingRoom()}
      ${WaitOrStart()}
	`;
}

export function setupTournamentMatching() {
  const jsonData = [
    { avatarPath: "/assets/user.png", name: "rikeda1" },
    { avatarPath: "/assets/user.png", name: "rikeda2" },
    { avatarPath: "/assets/user.png", name: "rikeda3" },
    { avatarPath: "/assets/user.png", name: "rikeda4" },
  ];

  renderMatchingRoom(jsonData);
  renderMatchingInfo(4, 16, 9);
  renderWaitOrStart("Wait...", "#0ca5bf");
}
