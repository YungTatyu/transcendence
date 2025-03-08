const GAME_HEIGHT = 500;
const GAME_WIDTH = 800;
const BALL_WIDTH = 20;
const BALL_HEIGHT = 20;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;

export default function Game() {
  function gameHeader() {
    return `
      <div class="game-header row mx-3 py-3">
        <div class="col-4 px-5 align-self-center">
          <div class="row py-1">
            <div class="player-name left-player-bgc col display-5 text-truncate rounded">
              player1
            </div>
          </div>
        </div>
        <div class="game-score text-white col-4 display-1 align-self-center">
          <span class="neon-text">00:01</span>
        </div>
        <div class="col-4 px-5 align-self-center">
          <div class="row py-1">
            <div class="player-name right-player-bgc col-auto display-5 text-truncate rounded">player2fdafdsafdsfdsf
            </div>
          </div>
        </div>
      </div>
      <div class="game-timer display-4">60</div>
    `
  };

  function gameCanvas() {
    return `
        <canvas class="game-canvas" width="${GAME_WIDTH}" height="${GAME_HEIGHT}"></canvas>
    `
  };


  return `
    <div class="game text-center bg-dark">
      ${gameHeader()}
      ${gameCanvas()}
    </div>
  `
};

export function drawGame() {
  const canvas = document.querySelector('.game-canvas');
  console.log(canvas);
  const ctx = canvas.getContext('2d');

  // ボールの描画
  const ball = {
    x: GAME_WIDTH / 2,
    y: GAME_HEIGHT / 2,
    width: BALL_WIDTH,
    height: BALL_HEIGHT,
    color: 'white',
  };
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.width / 2, 0, Math.PI * 2);
  ctx.fillStyle = ball.color;
  ctx.fill();
  ctx.closePath();

  // 左パドルの描画
  const leftPaddle = {
    x: 10,
    y: GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    color: '#0BB0CC',
  };
  ctx.fillStyle = leftPaddle.color;
  ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);

  // 右パドルの描画
  const rightPaddle = {
    x: GAME_WIDTH - 10 - PADDLE_WIDTH,
    y: GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    color: '#9F2BDA',
  };
  ctx.fillStyle = rightPaddle.color;
  ctx.fillRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);
};

