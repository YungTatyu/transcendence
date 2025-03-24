import TournamentBracket, {
  renderTournamentBracket,
} from "../services/tournament/TournamentBracket.js";
import { createTournamentData } from "../services/tournament/createTournamentData.js";
import WaitOrStart, { renderWaitOrStart } from "../components/WaitOrStart.js";

export default function Tournament() {
  return `
    <div class="match-vs d-flex justify-content-between w-100 mb-5 py-1 mt-5">
      <div class="w-50 text-center match-left-player px-5">rikeda1</div>
      <div class="d-flex justify-content-center align-items-center">
        <div class="diamond px-5 position-absolute bg-white d-flex justify-content-center align-items-center">
          <span class="diamond-text text-black text-center fw-bold">VS</span>
        </div>
      </div>
      <div class="w-50 text-center match-right-player px-5">rikeda2</div>
    </div>
    ${TournamentBracket()}
    ${WaitOrStart()}
  `;
}

export function setupTournament() {
  const tournamentJsonData = getTournamentJsonData();
  const tournamentData = createTournamentData(tournamentJsonData);
  renderTournamentBracket(tournamentData);
  renderWaitOrStart("WAIT...", "#0ca5bf");
}

function getTournamentJsonData() {
  const tournamentJsonStr = `
    {
      "matches_data": [
        {
          "matchId": 2,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": null,
          "round": 5,
          "participants": [
            {
              "id": 7,
              "score": null
            },
            {
              "id": 6,
              "score": null
            }
          ]
        },
        {
          "matchId": 2,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": null,
          "round": 2,
          "participants": [
            {
              "id": 3,
              "score": 10
            },
            {
              "id": 4,
              "score": -1
            }
          ]
        },
        {
          "matchId": 2,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": null,
          "round": 3,
          "participants": [
            {
              "id": 5,
              "score": 0
            },
            {
              "id": 6,
              "score": 11
            }
          ]
        },
        {
          "matchId": 2,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": null,
          "round": 6,
          "participants": [
            {
              "id": 2,
              "score": 0
            }
          ]
        },
        {
          "matchId": 2,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": null,
          "round": 4,
          "participants": [
            {
              "id": 3,
              "score":88 
            },
            {
              "id": 2,
              "score": 999
            }
          ]
        },
        {
          "matchId": 2,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": null,
          "round": 1,
          "participants": [
            {
              "id": 1,
              "score": 0
            },
            {
              "id": 2,
              "score": 1
            }
          ]
        }
      ],
      "current_round": 2,
      "state": "ongoing"
    }
  `;
  return JSON.parse(tournamentJsonStr);
}
