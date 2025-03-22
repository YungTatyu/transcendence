import TournamentBracket, {
  renderTournamentBracket,
} from "../components/TournamentBracket.js";
import { createTournamentData } from "../services/tournament/createTournamentData.js";

export default function Tournament() {
  return TournamentBracket();
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
              "score": null
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
              "score": null
            },
            {
              "id": 32792,
              "score": null
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
