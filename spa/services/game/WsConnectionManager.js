
const wsEventHandler = {
  handleOpen(message) {

  },
  handleMessage(message) {
  },

  handleClose(message) {

  },
  handleError(message) {

  }
}

export default class WsConnectionManager {
  constructor() {
    this.socket = null;
    this.eventHandler = wsEventHandler;
  }

  connect(matchId) {

  }

  disconnect() {

  }

  sendMessage(message) {

  }

  registerEventHandler() {
  }
}

