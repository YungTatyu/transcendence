import config from "../../config.js";

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected To Online Users List");
  },
  handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      const onlineUserList = parsedMessage.current_users;

      const dataTags = document.querySelectorAll(
        ".js-friend-list .user-status",
      );
      for (const dataTag of dataTags) {
        console.log(dataTag.dataset.userid);
        if (onlineUserList.includes(dataTag.dataset.userid)) {
          dataTag.textContent = "online";
          dataTag.style.color = "#0CC0DF";
        } else {
          dataTag.textContent = "offline";
          dataTag.style.color = "#929090";
        }
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

const WsFriendActivityManager = {
  socket: null,
  eventHandler: wsEventHandler,

  connect(accessToken) {
    this.socket = new WebSocket(
      `${config.friendActivityService}/friends/online`,
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

export default WsFriendActivityManager;
