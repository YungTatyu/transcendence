import config from "../../config.js";
import SPA from "../../spa.js";
import stateManager from "../../stateManager.js";

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to QuickPlay matching room");
  },
  async handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      const matchId = parsedMessage.match_id;
      const userIdList = parsedMessage.user_id_list;
      stateManager.setState({ players: userIdList });
      stateManager.setState({ matchId: matchId });
      // ユーザーが対戦相手を確認するためにSleepを挟む
      const sleep = (msec) =>
        new Promise((resolve) => setTimeout(resolve, msec));
      await sleep(1000);
      SPA.navigate("/game");
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

const WsTournamentMatchManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(accessToken, matchId) {
    this.socket = new WebSocket(
      `${config.matchMatchingService}/matches/ws/enter-room/${matchId}`,
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

export default WsTournamentMatchManager;
