import config from "../config.js";
import PlayerActionHandler from "../services/game/PlayerActionHandler.js";

const GAME_HEIGHT = 500;
const GAME_WIDTH = 800;
const GAME_LEFTEST = 0;
const BALL_WIDTH = 20;
const BALL_HEIGHT = 20;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;

export default function Game() {
  function gameHeader() {
    return `
    <div class="header-container">
      <div class="game-header row mx-3 pt-1 pb-0 mb-0">
        <div class="col-4 px-5 align-self-center">
          <div class="row py-1">
            <div class="player-name left-player-bgc col display-5 text-truncate rounded js-left-player">
              player1
            </div>
          </div>
        </div>
        <div class="game-score text-white col-4 display-1 align-self-center">
          <span class="neon-text js-game-score">00:00</span>
        </div>
        <div class="col-4 px-5 align-self-center">
          <div class="row py-1">
            <div class="player-name right-player-bgc col display-5 text-truncate rounded js-right-player">player2
            </div>
          </div>
        </div>
      </div>
      <h1 class="game-timer display-3 js-game-timer p-0 m-0">60</h1>
    </div>
    `;
  }

  function gameCanvas() {
    return `
      <div class="canvas-container d-flex justify-content-center align-items-center">
        <canvas class="game-canvas border border-2 border-white h-100" width="${GAME_WIDTH}" height="${GAME_HEIGHT}"></canvas>
      </div>
    `;
  }

  return `
    <div class="game text-center bg-dark vh-100">
      ${gameHeader()}
      ${gameCanvas()}
    </div>
  `;
}

export const gameRender = {
  renderGame(
    state = {
      ball: { x: GAME_WIDTH / 2, y: GAME_HEIGHT / 2 },
      leftPlayer: { id: "", y: GAME_HEIGHT / 2, score: 0 },
      rightPlayer: { id: "", y: GAME_HEIGHT / 2, score: 0 },
    },
  ) {
    const scoreEle = document.querySelector(".js-game-score");
    scoreEle.textContent = `${state.leftPlayer.score}:${state.rightPlayer.score}`;

    const canvas = document.querySelector(".game-canvas");
    const ctx = canvas.getContext("2d");

    const centerX = canvas.width / 2;

    ctx.setLineDash([15, 5]); // 5pxの線と5pxの間隔の点線
    ctx.lineWidth = 2; // 線の太さ
    ctx.strokeStyle = "#FFFFFF";

    // 垂直線を描画
    ctx.beginPath();
    ctx.moveTo(centerX, 0);
    ctx.lineTo(centerX, canvas.height);
    ctx.stroke();

    // ボールの描画
    const ball = {
      x: state.ball.x,
      y: state.ball.y,
      width: BALL_WIDTH,
      height: BALL_HEIGHT,
      color: "white",
    };
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.width / 2, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    ctx.closePath();

    // 左パドルの描画
    const leftPaddle = {
      x: GAME_LEFTEST,
      y: state.leftPlayer.y,
      width: PADDLE_WIDTH,
      height: PADDLE_HEIGHT,
      color: "#0BB0CC",
    };
    ctx.fillStyle = leftPaddle.color;
    ctx.fillRect(
      leftPaddle.x,
      leftPaddle.y,
      leftPaddle.width,
      leftPaddle.height,
    );

    // 右パドルの描画
    const rightPaddle = {
      x: GAME_WIDTH - PADDLE_WIDTH,
      y: state.rightPlayer.y,
      width: PADDLE_WIDTH,
      height: PADDLE_HEIGHT,
      color: "#9F2BDA",
    };
    ctx.fillStyle = rightPaddle.color;
    ctx.fillRect(
      rightPaddle.x,
      rightPaddle.y,
      rightPaddle.width,
      rightPaddle.height,
    );
  },
  renderTimer(time = 60) {
    const timerEle = document.querySelector(".js-game-timer");
    timerEle.textContent = time;
  },
  renderPlayerNames(players = []) {
    const nameClasses = [".js-left-player", ".js-left-player"];
    nameClasses.forEach((nameClass, index) => {
      const player = players[index];
      const element = document.querySelector(nameClass);

      if (element && player) {
        element.textContent = player.name;
      } else if (element) {
        element.textContent = "player";
      }
    });
  },
};

const fetchUsername = async (userid) => {
  const res = await fetch(`${config.userService}/users?userid=${userid}`);
  if (!res.ok) {
    throw new Error(`failed to fetch user data: ${res.status}`);
  }
  return await res.json().username;
};

export const setupGame = async () => {
  try {
    // TODO apiを叩くので一旦実行しない
    // const matchId = 1;
    // const res = await fetch(`${config.matchService}/matches?matchId=${matchId}`);
    // if (!res.ok) {
    //   throw new Error(`failed to fetch match data: ${res.status}`);
    // }
    // const match = await res.json().results[0];
    // const ids = match.participants.map((player) => player.id);
    // const gamePlayers = await Promise.all(ids.map(async (id) => await fetchUsername(id)));
    // gameRender.renderPlayerNames(gamePlayers);

    PlayerActionHandler.registerEventHandler();
    gameRender.renderGame();
  } catch (error) {
    console.error(error);
    // 配列を初期化する
    gamePlayers.splice(0, gamePlayers.length);
  }
};
