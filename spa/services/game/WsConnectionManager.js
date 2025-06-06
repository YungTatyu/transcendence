import config from "../../config.js";
import SPA from "../../spa.js";
import stateManager from "../../stateManager.js";
import { calcRemaingTime } from "../../utils/timerHelper.js";
import { gameRender } from "../../views/Game.js";

const startTimer = (endTime) => {
  const intervalId = setInterval(() => {
    const remainingTime = calcRemaingTime(endTime);
    gameRender.renderTimer(remainingTime);
    if (remainingTime <= 0) {
      clearInterval(intervalId);
    }
  }, 1000); // 1秒ごとに実行
  return intervalId;
};

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to game");
  },
  handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      const type = parsedMessage.type;
      const gameMessage = parsedMessage.message;
      if (type === "game.message" && gameMessage === "update") {
        const updatedState = parsedMessage.data.state;
        gameRender.renderGame({
          ball: updatedState.ball,
          leftPlayer: updatedState.left_player,
          rightPlayer: updatedState.right_player,
        });
      } else if (type === "game.message" && gameMessage === "timer") {
        // 対戦相手が再接続の際に、メッセージが送られる
        if (WsConnectionManager.intervalId !== null) {
          return;
        }
        const endTime = Number(parsedMessage.end_time) * 1000; // Unixタイム(秒) → ミリ秒に変換
        WsConnectionManager.intervalId = startTimer(endTime);
      } else if (type === "game.finish.message" && gameMessage === "gameover") {
        const results = parsedMessage.results;
        const highestScore = results.reduce((max, r) => {
          return r.score > max ? r.score : max;
        }, 0);
        const leftScore = results[0]?.score;
        const rightScore = results[1]?.score;
        const userId = stateManager.state?.userId;
        const win =
          userId &&
          results.some(
            (r) =>
              r.userId === Number.parseInt(userId, 10) &&
              r.score === highestScore,
          );
        SPA.navigate("/game/result", {
          left: leftScore,
          right: rightScore,
          win: win,
        });
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
    gameRender.renderError("failed to establish game connection.");
  },
};

const WsConnectionManager = {
  socket: null,
  eventHandler: wsEventHandler,
  intervalId: null,

  connect(matchId, accessToken) {
    this.socket = new WebSocket(
      `${config.realtimeGameService}/games/ws/enter-room/${matchId}`,
      ["app-protocol", accessToken],
    );
    this.registerEventHandler();
  },

  disconnect() {
    if (this.socket !== null) {
      this.socket.close();
      this.socket = null;
    }
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  },

  sendMessage(message) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error("Socket is not open. Unable to send message.");
      return;
    }
    this.socket.send(message);
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

export default WsConnectionManager;
