import config from "../../config.js";
import createTournamentData from "./createTournamentData.js";
import { renderTournamentBracket } from "./TournamentBracket.js";
import { renderPlayers, renderWinnerPlayer } from "./TournamentInfo.js";
import fetchPlayersData from "../../api/fetchPlayersData.js";
import { renderNeonInfo } from "../../components/NeonInfo.js";
import stateManager from "../../stateManager.js";
import WsTournamentMatchManager from "../match/WsTournamentMatchManager.js";
import fetchApiNoBody from "../../api/fetchApiNoBody.js";
import SPA from "../../spa.js";

const wsEventHandler = {
  canRender: true,
  parsedMessageChache: null,

  async renderTournament() {
    if (this.parsedMessageChache === null) {
      return;
    }
    const matchesData = this.parsedMessageChache.matches_data;
    const currentRound = this.parsedMessageChache.current_round;
    const state = this.parsedMessageChache.state;

    const tournamentData = createTournamentData(matchesData);
    renderTournamentBracket(tournamentData);

    switch (state) {
      case "ongoing":
        handleOngoing(matchesData, currentRound);
        break;
      case "error":
        renderNeonInfo("ERROR", "#FF0000");
        stateManager.state.tournamentId = null;
        console.error("Tournament error");
        break;
      case "finished": {
        const oldElement = document.getElementById("neon-info");
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

        const winnerPlayerName = await fetchWinnerPlayerName(matchesData);
        renderWinnerPlayer(winnerPlayerName);
        stateManager.state.tournamentId = null;
        break;
      }
    }
  },
  handleOpen(message) {
    console.log("Connected to Tournament room");
  },
  async handleMessage(message) {
    // データをキャッシュに保存し、描画可能なら描画する
    try {
      const parsedMessage = JSON.parse(message.data);
      this.parsedMessageChache = parsedMessage;
      if (this.canRender) {
        this.renderTournament();
      }
    } catch (error) {
      console.error("Failed to parse WebSocket message:", error);
    }
  },
  handleClose(message) {
    console.log("Disconnected from Tournament room");
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

  setCanRender(trueOrFalse) {
    this.eventHandler.canRender = trueOrFalse;
  },
  forceRenderTournament() {
    this.eventHandler.renderTournament();
  },
};

async function handleOngoing(matchesData, currentRound) {
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

export default WsTournamentManager;
