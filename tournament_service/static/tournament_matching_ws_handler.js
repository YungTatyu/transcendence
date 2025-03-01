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

		// トーナメント用WebSocketを作成
		this.tournamentWs = this.createTournamentWs(tournamentId);
	}

	handleDisplayTournamentStartTime(startTime) {
		if (startTime === "None") {
			this.timer.clear();
		} else {
			this.timer.start(startTime);
		}
	}

	createTournamentWs(tournamentId) {
		const ws = new WebSocket(
			`ws://localhost:8002/tournaments/ws/enter-room/${tournamentId}`,
		);
		ws.onmessage = (event) => {
			const matchesData = JSON.parse(event.data);
			const tournamentGraph = document.getElementById("tournamentGraph");
			const matchInfo = document.getElementById("matchInfo");
			tournamentGraph.textContent = JSON.stringify(matchesData, null, 2);
			matchInfo.textContent = this.getMatchVsInfo(matchesData);
		};
		ws.onerror = (error) => {
			console.error("Tournament WebSocket error:", error);
		};
		ws.onclose = () => {
			console.log("TournamentWs connection closed.");
		};
		return ws;
	}

	getMatchVsInfo(matchesData) {
		// current_round に一致する試合を抽出
		const currentRoundMatches = matchesData.matches_data.filter(
			match => match.round === matchesData.current_round
		);

		// 各試合の participants から id を取得し "XXX VS YYY" の形式に変換
		const matchStrings = currentRoundMatches.map(match => {
			const ids = match.participants.map(p => p.id);
			return `${ids[0]} VS ${ids[1]}`;
		});
		return matchStrings;
	}
}
