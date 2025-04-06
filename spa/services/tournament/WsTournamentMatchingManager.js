import fetchPlayersData from "../../api/fetchPlayersData.js";
import { renderMatchingRoom } from "../../components/MatchingRoom.js";
import { renderWaitOrStart } from "../../components/WaitOrStart.js";
import config from "../../config.js";
import SPA from "../../spa.js";
import stateManager from "../../stateManager.js";
import { renderMatchingInfo } from "./TournamentMatchingInfo.js";

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to QuickPlay matching room");
  },
  async handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      const tournamentId = parsedMessage.tournament_id;
      const userIdList = parsedMessage.wait_user_ids;
      const startTime = parsedMessage.tournament_start_time;

      const playersData = await fetchPlayersData(userIdList);
      renderMatchingRoom(playersData);
      renderMatchingInfo(userIdList.length, 16, startTime);

      if (tournamentId === undefined) {
        return;
      }
      if (tournamentId === "None") {
        console.error("TournamentId is None");
        return;
      }

      renderWaitOrStart("START", "#ffffff");
      stateManager.setState({ tournamentId: tournamentId });
      // ユーザーが対戦相手を確認するためにSleepを挟む
      const sleep = (msec) =>
        new Promise((resolve) => setTimeout(resolve, msec));
      await sleep(1000);
      SPA.navigate("/tournament");
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

const WsTournamentMatchingManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(accessToken) {
    this.socket = new WebSocket(
      `${config.tournamentMatchingService}/tournaments/ws/enter-room`,
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

export default WsTournamentMatchingManager;
