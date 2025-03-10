import { gameRender } from "../../views/Game.js";

const calcRemaingTime = (endTime) => {
  const now = Date.now(); // 現在時刻（ミリ秒）
  const re = Math.max(0, Math.floor((endTime - now) / 1000)); // 残り時間（秒単位）
  return re;
};

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
    console.log(`Connected to match`);
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
      }
      else if (
        parsedMessage.type === "game.message" &&
        parsedMessage.message === "timer"
      ) {
        const endTime = Number(parsedMessage.end_time) * 1000; // Unixタイム(秒) → ミリ秒に変換
        startTimer(endTime);
      }
      else if (
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

  connect(matchId) { },

  disconnect() { },

  sendMessage(message) { },

  registerEventHandler() { },
};

export default WsConnectionManager;
