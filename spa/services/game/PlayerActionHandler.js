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

  }

  registerEventHandler() {
    document.addEventListener("keydown", this.handleKeyAction);
    document.addEventListener("keyup", this.handleKeyAction);
  }
}
