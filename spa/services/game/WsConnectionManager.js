
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

const WsConnectionManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(matchId) {

  },

  disconnect() {

  },

  sendMessage(message) {

  },

  registerEventHandler() {
  },
}

export default WsConnectionManager;
