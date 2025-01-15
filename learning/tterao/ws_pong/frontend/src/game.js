
// ゲームの定数
const GAME_HEIGHT = 500;
const GAME_WIDTH = 800;
const BALL_WIDTH = 20;
const BALL_HEIGHT = 20;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;

// キャンバス初期化
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
canvas.width = GAME_WIDTH;
canvas.height = GAME_HEIGHT;

// ゲーム状態
let gameState = {
  ball: { x: GAME_WIDTH / 2, y: GAME_HEIGHT / 2 },
  leftPlayer: { y: (GAME_HEIGHT - PADDLE_HEIGHT) / 2, score: 0 },
  rightPlayer: { y: (GAME_HEIGHT - PADDLE_HEIGHT) / 2, score: 0 },
};

const keys = {
  // KeyK: false,
  // KeyJ: false,
  KeyW: false,
  KeyS: false
};

// WebSocket変数
let ws;

let username;

// WebSocketで取得したデータを描画
function draw() {
  // 背景クリア
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

  // ボール描画
  ctx.fillStyle = "white";
  ctx.fillRect(
    gameState.ball.x,
    gameState.ball.y,
    BALL_WIDTH,
    BALL_HEIGHT
  );

  // 左プレイヤーのパドル描画
  ctx.fillRect(
    0,
    gameState.leftPlayer.y,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
  );

  // 右プレイヤーのパドル描画
  ctx.fillRect(
    GAME_WIDTH - PADDLE_WIDTH,
    gameState.rightPlayer.y,
    PADDLE_HEIGHT,
    PADDLE_HEIGHT
  );

  // スコア描画
  ctx.fillStyle = "white";
  ctx.font = "20px Arial";
  ctx.fillText(`Player 1: ${gameState.leftPlayer.score}`, 20, 30);
  ctx.fillText(
    `Player 2: ${gameState.rightPlayer.score}`,
    GAME_WIDTH - 140,
    30
  );
}

// WebSocketメッセージの受信
function setupWebSocket(matchId, username) {
  ws = new WebSocket(`ws://localhost:8000/ws/game/${matchId}/${username}`);

  ws.onopen = (event) => {
    console.log("ws connection established.", event)
  }
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "game.message" && message.message === "game update") {
      const state = message.data.state;
      gameState = {
        ball: { x: state.ball.x, y: state.ball.y },
        leftPlayer: {
          y: state.aa.y, // 左プレイヤー
          score: state.aa.score,
        },
        rightPlayer: {
          y: state.bb.y, // 右プレイヤー
          score: state.bb.score,
          // score: state[Object.keys(state)[2]].score,
        },
      };
      draw();
    }
  };

  ws.onclose = (event) => {
    console.log("The connection has been closed successfully.", event);
  };

  ws.onerror = (error) => {
    console.error("WebSocket Error:", error);
  };
}

// スタートボタンのクリックイベント
document.getElementById("startGame").addEventListener("click", () => {
  username = document.getElementById("username").value.trim();
  if (!username) {
    alert("Please enter a username.");
    return;
  }

  const matchId = 1; // 任意の試合ID
  setupWebSocket(matchId, username);
  draw(); // 初期状態描画
});

document.addEventListener('keydown', (e) => {
  console.log("keydown event", e.code)
  if (keys.hasOwnProperty(e.code)) {
    keys[e.code] = true;
    sendKeyInputToServer(e.code); // キーが押された状態を送信
  }
});

document.addEventListener('keyup', (e) => {
  console.log("keyup event", e.code)
  if (keys.hasOwnProperty(e.code)) {
    keys[e.code] = false;
  }
});

function sendKeyInputToServer(key) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    const message = JSON.stringify({
      type: "game.paddle_move", // メッセージのタイプ
      key: key,      // 押されたキー (例: "KeyW")
      username: username,   // ユーザー名（必要なら送信）
    });
    console.log("sending", message)
    ws.send(message);
  } else {
    console.warn("WebSocket is not open. Unable to send key input.");
  }
}
