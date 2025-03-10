import WsConnectionManager from "./WsConnectionManager.js";

const UP_KEY = "upKey";
const DOWN_KEY = "downKey";

export default class PlayerActionHandler {
  constructor() {
    this.actionKeys = {
      UP_KEY: "KeyW",
      DOWN_KEY: "KeyS",
    }
  }

  handleKeyAction(event) {
    if (!Object.values(this.actionKeys).includes(event.code)) {
      return;
    }

  }

  registerEventHandler() {
    document.addEventListener("keydown", this.handleKeyAction);
    document.addEventListener("keyup", this.handleKeyAction);
  }

  cleanup() {
    document.removeEventListener("keydown", this.handleKeyAction);
    document.removeEventListener("keyup", this.handleKeyAction);
  }
}
