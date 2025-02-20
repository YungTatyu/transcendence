class TournamentMatchingWsHandler {
  /**
   * @param {string} url トーナメントマッチング機能のエンドポイント
   * @param {HTMLElement} startTimeElement タイマーを表示するHTML要素
   */
  constructor(url, startTimeElement) {
    this.webSocketUrl = url;
    this.startTimeElement = startTimeElement;
    this.timer = new CountDownTimer(startTimeElement);
    this.ws = null;
  }

  // TournamentMatchingへのWebSocket接続を開始する
  connect() {
    this.ws = new WebSocket(this.webSocketUrl);

    // WebSocketからのメッセージの受信時
    this.ws.onmessage = (event) => {
      this.handleMessage(event);
    };

    // WebSocketでのエラー発生時
    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.timer.clear();
    };

    // WebSocket切断時
    this.ws.onclose = () => {
      console.log("WebSocket connection closed.");
      // this.timer.clear();
    };
  }

  handleMessage(event) {
    const sentData = JSON.parse(event.data);
    console.log(
      "recieve",
      sentData.tournament_id,
      sentData.tournament_start_time,
      sentData.wait_user_ids,
    );

    if (sentData.tournament_id) {
      this.handleStartTournament(sentData.tournament_id);
    } else if (sentData.tournament_start_time) {
      this.handleDisplayTournamentStartTime(sentData.tournament_start_time);
    } else {
      console.log("Error: Unknown data received.");
    }
  }

  handleStartTournament(tournamentId) {
    console.log(`Tournament ID: ${tournamentId}`);
    this.timer.clear();
    // トーナメントマッチングルーム用WebSocketは削除
    this.ws.close();
    // TODO トーナメント用WebSocketを作成
  }

  handleDisplayTournamentStartTime(startTime) {
    if (startTime === "None") {
      this.timer.clear();
    } else {
      this.timer.start(startTime);
    }
  }
}
