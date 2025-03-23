import TournamentBracket, {
  renderTournamentBracket,
} from "../services/tournament/TournamentBracket.js";
import { createTournamentData } from "../services/tournament/createTournamentData.js";

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
  `;
}

export function setupTournament() {
  const tournamentJsonData = getTournamentJsonData();
  const tournamentData = createTournamentData(tournamentJsonData);
  renderTournamentBracket(tournamentData);
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
          "round": 3,
          "participants": [
            {
              "id": 41650,
              "score": 0
            },
            {
              "id": 32792,
              "score": 1
            }
          ]
        },
        {
          "matchId": 3,
          "winnerUserId": 41650,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": 2,
          "round": 1,
          "participants": [
            {
              "id": 41650,
              "score": 0
            },
            {
              "id": 32790,
              "score": -1
            }
          ]
        },
        {
          "matchId": 4,
          "winnerUserId": null,
          "mode": "Tournament",
          "tournamentId": 2,
          "parentMatchId": 2,
          "round": 2,
          "participants": [
            {
              "id": 32774,
              "score": 0
            },
            {
              "id": 32792,
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
