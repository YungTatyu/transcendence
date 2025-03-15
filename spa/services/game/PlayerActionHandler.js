import stateManager from "../../stateManager.js";
import WsConnectionManager from "./WsConnectionManager.js";

const PlayerActionHandler = {
  actionKeys: {
    upKey: "KeyW",
    downKey: "KeyS",
  },
  handleKeyAction(event) {
    if (!Object.values(PlayerActionHandler.actionKeys).includes(event.code)) {
      return;
    }
    const message = JSON.stringify({
      type: "game.paddle_move",
      key: e.code,
      userid: stateManager.state?.userId,
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
};

export default PlayerActionHandler;
