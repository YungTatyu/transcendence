import fetchPlayersData from "../../api/fetchPlayersData.js";
import { renderMatchingRoom } from "../../components/MatchingRoom.js";
import { renderNeonInfo } from "../../components/NeonInfo.js";
import config from "../../config.js";
import SPA from "../../spa.js";
import stateManager from "../../stateManager.js";
import { calcRemaingTime } from "../../utils/timerHelper.js";
import { renderMatchingInfo, renderTimer } from "./TournamentMatchingInfo.js";
import WsTournamentManager from "./WsTournamentManager.js";

const startTimer = (endTime) => {
  const intervalId = setInterval(() => {
    const remainingTime = calcRemaingTime(endTime);
    renderTimer(remainingTime);
    if (remainingTime <= 0) {
      clearInterval(intervalId);
    }
  }, 1000); // 1秒ごとに実行
  return intervalId;
};

const wsEventHandler = {
  handleOpen(message) {
    console.log("Connected to Tournament matching room");
  },
  async handleMessage(message) {
    try {
      const parsedMessage = JSON.parse(message.data);
      const tournamentId = parsedMessage.tournament_id;
      const userIdList = parsedMessage.wait_user_ids;
      const roomCapacity = parsedMessage.room_capacity;
      const startTime = parsedMessage.tournament_start_time;

      // INFO 必ずタイマーをClearする
      clearInterval(WsTournamentMatchingManager.intervalId);

      // INFO startTimeがNoneならTimerをリセット
      if (startTime === "None") {
        renderTimer("-");
      } else {
        const endTime = Number(startTime) * 1000; // Unixタイム(秒) → ミリ秒に変換
        WsTournamentMatchingManager.intervalId = startTimer(endTime);
      }

      const playersData = await fetchPlayersData(userIdList);
      if (playersData === null) {
        return;
      }
      renderMatchingRoom(playersData);
      renderMatchingInfo(userIdList.length, roomCapacity);

      if (tournamentId === undefined) {
        return;
      }
      if (tournamentId === "None") {
        console.error("TournamentId is None");
        return;
      }

      renderNeonInfo("START", "#ffffff");
      // INFO 稼働していないintervalIdに対して実行しても問題ない
      clearInterval(WsTournamentMatchingManager.intervalId);
      // INFO 古いWebSocketConnectionを削除
      WsTournamentManager.disconnect();
      stateManager.setState({ tournamentId: tournamentId });
      // ユーザーが対戦相手を確認するためにSleepを挟む
      const sleep = (msec) =>
        new Promise((resolve) => setTimeout(resolve, msec));
      await sleep(1000);
      SPA.navigate("/tournament");
    } catch (error) {
      console.error("Failed to parse WebSocket message:", error);
    }
  },
  handleClose(message) {
    console.log("Disconnected from Tournament matching room");
  },
  handleError(message) {
    console.error("WebSocket error:", message);
  },
};

const WsTournamentMatchingManager = {
  socket: null,
  eventHandler: wsEventHandler,
  intervalId: null,

  connect(accessToken) {
    this.socket = new WebSocket(
      `${config.tournamentMatchingService}/tournaments/ws/enter-room`,
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

  registerEventHandler() {
    this.socket.onopen = this.eventHandler.handleOpen.bind(this.eventHandler);
    this.socket.onmessage = this.eventHandler.handleMessage.bind(
      this.eventHandler,
    );
    this.socket.onclose = this.eventHandler.handleClose.bind(this.eventHandler);
    this.socket.onerror = this.eventHandler.handleError.bind(this.eventHandler);
  },
};

export default WsTournamentMatchingManager;
