import fetchApiNoBody from "../../api/fetchApiNoBody.js";
import fetchPlayersData from "../../api/fetchPlayersData.js";
import { renderNeonInfo } from "../../components/NeonInfo.js";
import config from "../../config.js";
import SPA from "../../spa.js";
import stateManager from "../../stateManager.js";
import WsTournamentMatchManager from "../match/WsTournamentMatchManager.js";
import { renderPlayers, renderWinnerPlayer } from "./TournamentInfo.js";

export async function ongoingStateHandler(matchesData, currentRound) {
  const participantsForRound = matchesData
    .filter((match) => match.round === currentRound)
    .map((match) => match.participants)[0];
  const matchId = matchesData
    .filter((match) => match.round === currentRound)
    .map((match) => match.matchId)[0];
  const playersId = participantsForRound.map((participant) => participant.id);

  const playersData = await fetchPlayersData(playersId);
  if (playersData === null) {
    return;
  }
  renderPlayers(playersData[0].name, playersData[1].name);

  if (playersId.includes(Number(stateManager.state.userId))) {
    renderNeonInfo("START", "#FFFFFF");
    prepareTournamentMatch(matchId);
  } else {
    renderNeonInfo("WAIT...", "#0ca5bf");
  }

  function prepareTournamentMatch(matchId) {
    try {
      const accessToken = sessionStorage.getItem("access_token");
      if (!(accessToken && matchId)) {
        console.error("Error prepareTournamentMatch");
        return;
      }
      WsTournamentMatchManager.disconnect();
      WsTournamentMatchManager.connect(accessToken, matchId);
    } catch (error) {
      console.error(error);
    }
  }
}

export async function errorStateHandler() {
  renderNeonInfo("ERROR", "#FF0000");
  stateManager.setState({ tournamentId: null });
  console.error("Tournament error");
}

export async function finishedStateHandler(matchesData) {
  replaceNeonInfoToBackToHomeButton();
  const winnerPlayerName = await fetchWinnerPlayerName(matchesData);
  renderWinnerPlayer(winnerPlayerName);
  stateManager.setState({ tournamentId: null });
  WsTournamentMatchManager.disconnect();
  return;

  async function fetchWinnerPlayerName(matchesData) {
    const winnerUserId = matchesData.reduce((latestMatch, currentMatch) => {
      return currentMatch.round > latestMatch.round
        ? currentMatch
        : latestMatch;
    }).winnerUserId;
    const winnerUser = await fetchApiNoBody(
      "GET",
      config.userService,
      `/users?userid=${winnerUserId}`,
    );

    // UserNameの取得に失敗したらIDを返す
    if (winnerUser.status === null || winnerUser.status >= 400) {
      return winnerUserId;
    }
    return winnerUser.data.username;
  }
}

export function replaceNeonInfoToBackToHomeButton() {
  const oldElement = document.getElementById("neon-info");
  if (!oldElement) {
    return;
  }
  const wrapper = document.createElement("div");
  wrapper.className = "d-flex justify-content-center";

  const newElement = document.createElement("button");
  newElement.type = "button";
  newElement.className = "my-5 py-3 px-5 tournament-result-button";
  newElement.textContent = "Back To Home";
  newElement.addEventListener("click", (event) => {
    event.preventDefault();
    SPA.navigate("/home", null, true);
  });
  wrapper.appendChild(newElement);
  oldElement.replaceWith(wrapper);
}
