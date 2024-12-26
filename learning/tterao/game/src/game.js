
const PLAYER_ONE = "player1"
const PLAYER_TWO = "player2"
const game = document.getElementById('game');
const ball = document.getElementById('ball');
const paddle1 = document.getElementById('paddle1');
const paddle2 = document.getElementById('paddle2');

// 初期位置と速度
let ballX = 390, ballY = 240; // ボールの初期位置
let ballSpeedX = 4, ballSpeedY = 4; // ボールの速度
let paddle1Y = 200, paddle2Y = 200; // パドルの初期位置
const paddleSpeed = 10;

// ゲームエリアの制限
const gameHeight = game.clientHeight;
const paddleHeight = paddle1.clientHeight;

// キーボード入力状態
const keys = {
  KeyK: false,
  KeyJ: false,
  KeyW: false,
  KeyS: false
};

const score = {
  player1: 0,
  player2: 0,
}

// ゲーム状態の初期化
const gameState = {
  player1: PLAYER_ONE,
  player2: PLAYER_TWO,
  score1: 0,
  score2: 0,
  timer: 60,
};

// キーボードイベント
document.addEventListener('keydown', (e) => {
  if (keys.hasOwnProperty(e.code)) keys[e.code] = true;
});
document.addEventListener('keyup', (e) => {
  if (keys.hasOwnProperty(e.code)) keys[e.code] = false;
});

// DOM 要素を取得
const player1Element = document.querySelector('.js-player1');
const player2Element = document.querySelector('.js-player2');
const scoreElement = document.querySelector('.js-score');
const timerElement = document.querySelector('.js-timer');

// ゲーム情報を表示
function updateGameInfo() {
  player1Element.textContent = `${gameState.player1}`;
  player2Element.textContent = `${gameState.player2}`;
  scoreElement.textContent = `${gameState.score1} - ${gameState.score2}`;
  timerElement.textContent = `${gameState.timer}`;
}

// タイマーを開始
function startTimer() {
  const timerInterval = setInterval(() => {
    if (gameState.timer > 0) {
      gameState.timer -= 1;
      updateGameInfo();
    } else {
      clearInterval(timerInterval);
      alert("Game Over!");
    }
  }, 1000);
}


// ゲームループ
function gameLoop() {
  // パドルの移動
  if (keys.KeyW && paddle1Y > 0) paddle1Y -= paddleSpeed;
  if (keys.KeyS && paddle1Y < gameHeight - paddleHeight) paddle1Y += paddleSpeed;
  if (keys.KeyK && paddle2Y > 0) paddle2Y -= paddleSpeed;
  if (keys.KeyJ && paddle2Y < gameHeight - paddleHeight) paddle2Y += paddleSpeed;

  paddle1.style.top = paddle1Y + 'px';
  paddle2.style.top = paddle2Y + 'px';

  // ボールの移動
  ballX += ballSpeedX;
  ballY += ballSpeedY;

  // 壁で跳ね返る
  if (ballY <= 0 || ballY >= gameHeight - 20) ballSpeedY *= -1;

  // パドルで跳ね返る
  if (
    (ballX <= 20 && ballY + 20 >= paddle1Y && ballY <= paddle1Y + paddleHeight) ||
    (ballX >= 760 && ballY + 20 >= paddle2Y && ballY <= paddle2Y + paddleHeight)
  ) {
    ballSpeedX *= -1 * 1.2;
  }

  // スコアリセット (ゲームオーバー)
  if (ballX <= 0 || ballX >= 780) {
    if (ballX <= 0) gameState.score1 += 1;
    else gameState.score2 += 1;
    ballX = 390;
    ballY = 240;
    ballSpeedX = 4 * (Math.random() > 0.5 ? 1 : -1);
    ballSpeedY = 4 * (Math.random() > 0.5 ? 1 : -1);
  }

  ball.style.left = ballX + 'px';
  ball.style.top = ballY + 'px';

  requestAnimationFrame(gameLoop);
}

// 初期表示
updateGameInfo();
startTimer();
gameLoop();
