import fetchApiNoBody from "../../api/fetchApiNoBody.js";
import { renderMatchingRoom } from "../../components/MatchingRoom.js";
import { renderWaitOrStart } from "../../components/WaitOrStart.js";
import config from "../../config.js";

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
      if (parsedMessage !== "None") {
        const playersData = await fetchPlayersData(userIdList);
        console.log(playersData);
        renderMatchingRoom(playersData);
        renderWaitOrStart("START", "#ffffff");
        changeMatchingInfo();
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

function changeMatchingInfo() {
  const matchingInfo = document.getElementById("matching-info");

  matchingInfo.innerHTML = "OPPONENT FOUND.";
  matchingInfo.style.color = "#0CC0DF";
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
