import config from "../../config.js";
import { renderTournamentBracket } from "./TournamentBracket.js";
import createTournamentData from "./createTournamentData.js";
import {
  errorStateHandler,
  finishedStateHandler,
  ongoingStateHandler,
  replaceNeonInfoToBackToHomeButton,
} from "./tournamentStateHandler.js";

const wsEventHandler = {
  canRender: true,
  parsedMessageChache: null,

  async renderTournament() {
    try {
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
          ongoingStateHandler(matchesData, currentRound);
          break;
        case "error":
          errorStateHandler();
          break;
        case "finished":
          finishedStateHandler(matchesData);
          break;
      }
    } catch (error) {
      console.log(error);
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
    replaceNeonInfoToBackToHomeButton();
    stateManager.setState({ tournamentId: null });
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

export default WsTournamentManager;
