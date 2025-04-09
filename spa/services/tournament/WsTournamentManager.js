import config from "../../config.js";
import createTournamentData from "./createTournamentData.js";
import { renderTournamentBracket } from "./TournamentBracket.js";
import { renderPlayers } from "./TournamentInfo.js";
import fetchPlayersData from "../../api/fetchPlayersData.js";
import { renderWaitOrStart } from "../../components/WaitOrStart.js";
import stateManager from "../../stateManager.js";

async function handleTournament(matchesData, currentRound) {
  const participantsForRound = matchesData
    .filter((match) => match.round === currentRound)
    .map((match) => match.participants);
  const playersId = participantsForRound[0].map(
    (participant) => participant.id,
  );

  const playersData = await fetchPlayersData(playersId);
  if (!playersData) {
    return;
  }
  renderPlayers(playersData[0].name, playersData[1].name);

  // INFO 次の試合参加者ならSTART、そうでないならWAITを描画
  if (playersId.includes(Number(stateManager.state.userId))) {
    renderWaitOrStart("START", "#FFFFFF");
  } else {
    renderWaitOrStart("WAIT...", "#0ca5bf");
  }
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
          renderWaitOrStart("ERROR", "#FF0000");
          console.error("Tournament error");
          break;
        case "finished":
          renderWaitOrStart("FINISHED", "#FFFF00");
          console.log("Tournament finished");
          break;
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
