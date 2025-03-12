import config from "../../config.js";
import { calcRemaingTime } from "../../utils/timerHelper.js";
import { gameRender } from "../../views/Game.js";

const startTimer = (endTime) => {
  const interval = setInterval(() => {
    const remainingTime = calcRemaingTime(endTime);
    gameRender.renderTimer(remainingTime);
    if (time <= 0) {
      clearInterval(interval);
    }
  }, 1000); // 1秒ごとに実行
};

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to match");
  },
  handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      if (
        parsedMessage.type === "game.message" &&
        parsedMessage.message === "update"
      ) {
        const updatedState = parsedMessage.data.state;
        gameRender.renderGame(updatedState);
      } else if (
        parsedMessage.type === "game.message" &&
        parsedMessage.message === "timer"
      ) {
        const endTime = Number(parsedMessage.end_time) * 1000; // Unixタイム(秒) → ミリ秒に変換
        startTimer(endTime);
      } else if (
        parsedMessage.type === "game.finish.message" &&
        parsedMessage.message === "gameover"
      ) {
        const results = parsedMessage.results;
        alert(
          `game·over:\n${results.map((r) => `User ${r.userId}: ${r.score}`).join("\n")}`,
        );
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

const WsConnectionManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(matchId) {
    this.socket = new WebSocket(
      `ws://${config.gameService}/games/ws/enter-room/${matchId}`,
    );
  },

  disconnect() {
    if (this.socket === null) {
      return;
    }
    this.socket.close();
    this.socket = null;
  },

  sendMessage(message) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error("Socket is not open. Unable to send message.");
      return;
    }
    this.socket.send(message);
  },

  registerEventHandler() {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error("Socket is not open. Unable to send message.");
      return;
    }
    this.socket.onopen = this.eventHandler.handleOpen.bind(this.eventHandler);
    this.socket.onmessage = this.eventHandler.handleMessage.bind(
      this.eventHandler,
    );
    this.socket.onclose = this.eventHandler.handleClose.bind(this.eventHandler);
    this.socket.onerror = this.eventHandler.handleError.bind(this.eventHandler);
  },
};

export default WsConnectionManager;
