import WsConnectionManager from "./WsConnectionManager.js";

const UP_KEY = "upKey";
const DOWN_KEY = "downKey";

const PlayerActionHandler = {
  actionKeys: {
    UP_KEY: "KeyW",
    DOWN_KEY: "KeyS",
  },
  handleKeyAction(event) {
    if (!Object.values(this.actionKeys).includes(event.code)) {
      return;
    }
    const message = JSON.stringify({
      type: "game.paddle_move",
      key: e.code,
      // userid: userid,
    });
    WsConnectionManager.sendMessage(message);
  },
  registerEventHandler() {
    document.addEventListener("keydown", this.handleKeyAction);
    document.addEventListener("keyup", this.handleKeyAction);
  },
  cleanup() {
    document.removeEventListener("keydown", this.handleKeyAction);
    document.removeEventListener("keyup", this.handleKeyAction);
  },
}

export default PlayerActionHandler;
