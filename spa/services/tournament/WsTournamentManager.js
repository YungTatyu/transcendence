import config from "../../config.js";
import createTournamentData from "./createTournamentData.js";
import { renderTournamentBracket } from "./TournamentBracket.js";
import { renderPlayers, renderWinnerPlayer } from "./TournamentInfo.js";
import fetchPlayersData from "../../api/fetchPlayersData.js";
import { renderNeonInfo } from "../../components/NeonInfo.js";
import stateManager from "../../stateManager.js";
import WsTournamentMatchManager from "../match/WsTournamentMatchManager.js";
import fetchApiNoBody from "../../api/fetchApiNoBody.js";

async function handleTournament(matchesData, currentRound) {
  const participantsForRound = matchesData
    .filter((match) => match.round === currentRound)
    .map((match) => match.participants)[0];
  const matchId = matchesData
    .filter((match) => match.round === currentRound)
    .map((match) => match.matchId)[0];
  const playersId = participantsForRound.map((participant) => participant.id);

  const playersData = await fetchPlayersData(playersId);
  if (!playersData) {
    return;
  }
  renderPlayers(playersData[0].name, playersData[1].name);

  // INFO 次の試合参加者ならSTART、そうでないならWAITを描画
  if (playersId.includes(Number(stateManager.state.userId))) {
    renderNeonInfo("START", "#FFFFFF");
    prepareTournamentMatch(matchId);
  } else {
    renderNeonInfo("WAIT...", "#0ca5bf");
  }
}

function prepareTournamentMatch(matchId) {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!(accessToken && matchId)) {
      console.error("Error prepareTournamentMatch");
      return;
    }
    WsTournamentMatchManager.connect(accessToken, matchId);
  } catch (error) {
    console.error(error);
  }
}

async function fetchWinnerPlayerName(matchesData) {
  const winnerUserId = matchesData.reduce((latestMatch, currentMatch) => {
    return currentMatch.round > latestMatch.round ? currentMatch : latestMatch;
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

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to QuickPlay matching room");
  },
  async handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      const matchesData = parsedMessage.matches_data;
      const currentRound = parsedMessage.current_round;
      const state = parsedMessage.state;

      const tournamentData = createTournamentData(matchesData);
      renderTournamentBracket(tournamentData);

      switch (state) {
        case "ongoing":
          handleTournament(matchesData, currentRound);
          break;
        case "error":
          renderNeonInfo("ERROR", "#FF0000");
          stateManager.state.tournamentId = null;
          console.error("Tournament error");
          break;
        case "finished": {
          renderNeonInfo("FINISHED", "#FFFF00");
          const winnerPlayerName = await fetchWinnerPlayerName(matchesData);
          renderWinnerPlayer(winnerPlayerName);
          stateManager.state.tournamentId = null;
          console.log("Tournament finished");
          break;
        }
      }
    } catch (error) {
      console.error("Failed to parse WebSocket message:", error);
    }
  },
  handleClose(message) {
    console.log("Disconnected from server");
  },
  handleError(message) {
    console.error("WebSocket error:", message);
  },
};

const WsTournamentManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(accessToken, tournamentId) {
    this.socket = new WebSocket(
      `${config.tournamentMatchingService}/tournaments/ws/enter-room/${tournamentId}`,
      ["app-protocol", accessToken],
    );
    this.registerEventHandler();
  },

  disconnect() {
    if (this.socket !== null) {
      this.socket.close();
      this.socket = null;
    }
  },

  registerEventHandler() {
    this.socket.onopen = this.eventHandler.handleOpen.bind(this.eventHandler);
    this.socket.onmessage = this.eventHandler.handleMessage.bind(
      this.eventHandler,
    );
    this.socket.onclose = this.eventHandler.handleClose.bind(this.eventHandler);
    this.socket.onerror = this.eventHandler.handleError.bind(this.eventHandler);
  },
};

export default WsTournamentManager;
