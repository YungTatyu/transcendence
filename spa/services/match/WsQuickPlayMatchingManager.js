import fetchApiNoBody from "../../api/fetchApiNoBody.js";
import { renderMatchingRoom } from "../../components/MatchingRoom.js";
import { renderWaitOrStart } from "../../components/WaitOrStart.js";
import config from "../../config.js";
import SPA from "../../spa.js";
import stateManager from "../../stateManager.js";
import { renderMatchingInfo } from "./MatchingInfo.js";

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to QuickPlay matching room");
  },
  async handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      console.log(parsedMessage);
      const matchId = parsedMessage.match_id;
      const userIdList = parsedMessage.user_id_list;
      const playersData = await fetchPlayersData(userIdList);
      renderMatchingRoom(playersData);
      if (matchId === undefined) {
        return;
      }
      if (matchId === "None") {
        renderMatchingInfo("Error occurred", "#FF0000");
        return;
      }
      renderWaitOrStart("START", "#ffffff");
      renderMatchingInfo("OPPONENT FOUND.", "#0CC0DF");
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

async function fetchPlayersData(userIdList) {
  try {
    const promises = userIdList.map((id) =>
      fetchApiNoBody("GET", config.userService, `/users?userid=${id}`),
    );
    const results = await Promise.all(promises);
    const playersData = results.map((item) => ({
      avatarPath: `${config.userService}/${item.data.avatarPath}`,
      name: item.data.username,
    }));
    return playersData;
  } catch (error) {
    console.error("Error");
  }
}

const WsQuickPlayMatchingManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(accessToken) {
    this.socket = new WebSocket(
      `${config.matchMatchingService}/matches/ws/enter-room`,
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

export default WsQuickPlayMatchingManager;
