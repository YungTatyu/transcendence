import config from "../../config.js";
import createTournamentData from "./createTournamentData.js";
import { renderTournamentBracket } from "./TournamentBracket.js";

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

      console.log("matchesData: ", matchesData);
      console.log("currentRound: ", currentRound);
      console.log("state: ", state);

      const tournamentData = createTournamentData(matchesData);
      renderTournamentBracket(tournamentData);
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
