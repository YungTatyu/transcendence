import config from "../config.js";
import PlayerActionHandler from "../services/game/PlayerActionHandler.js";
import WsConnectionManager from "../services/game/WsConnectionManager.js";
import SPA from "../spa.js";
import stateManager from "../stateManager.js";

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
            </div>
          </div>
        </div>
        <div class="game-score text-white col-4 display-1 align-self-center">
          <span class="neon-text js-game-score">00:00</span>
        </div>
        <div class="col-4 px-5 align-self-center">
          <div class="row py-1">
            <div class="player-name right-player-bgc col display-5 text-truncate rounded js-right-player">
            </div>
          </div>
        </div>
      </div>
      <h1 class="game-timer display-3 js-game-timer p-0 m-0">60</h1>
      <h1 class="js-game-error fs-1 text-center text-danger fw-bold text-wrap"></h1>
      <p class="js-game-error-detail fs-2 text-center text-danger text-wrap"></p>
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
    <div class="game text-center bg-black vh-100">
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
    if (scoreEle === null) {
      return
    }
    scoreEle.textContent = `${state.leftPlayer.score}:${state.rightPlayer.score}`;

    const canvas = document.querySelector(".game-canvas");
    if (canvas === null) {
      return
    }
    const ctx = canvas.getContext("2d");

    // 背景クリア
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

    ctx.setLineDash([15, 5]); // 5pxの線と5pxの間隔の点線
    ctx.lineWidth = 2; // 線の太さ
    ctx.strokeStyle = "#FFFFFF";

    // 垂直線を描画
    ctx.beginPath();
    const centerX = canvas.width / 2;
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
    ctx.arc(
      ball.x + ball.width / 2,
      ball.y + ball.height / 2,
      ball.width / 2,
      0,
      Math.PI * 2,
    );
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
    if (timerEle) {
      timerEle.textContent = time;
    }
  },
  renderPlayerNames(players = []) {
    const nameClasses = [".js-left-player", ".js-right-player"];
    nameClasses.forEach((nameClass, index) => {
      const playerName = players[index] ?? "";
      const element = document.querySelector(nameClass);
      if (element) {
        element.textContent = playerName;
      }
    });
  },
  renderError(errMessage) {
    const canvas = document.querySelector(".game-canvas");
    // 画面をクリア
    if (canvas) {
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    const errEle = document.querySelector(".js-game-error");
    const errDetail = document.querySelector(".js-game-error-detail");
    if (errEle) {
      errEle.textContent = "Error occured.";
    }
    if (errDetail) {
      errDetail.textContent = errMessage;
    }
  },
};

const fetchUsername = async (userid) => {
  const res = await fetch(`${config.userService}/users?userid=${userid}`);
  if (!res.ok) {
    throw new Error(`failed to fetch user data: ${res.status}`);
  }
  const data = await res.json();
  return data.username;
};

export const setupGame = async () => {
  try {
    if (!stateManager.state?.players || !stateManager.state?.matchId) {
      SPA.navigate("/");
      return;
    }
    gameRender.renderGame();
    const names = await Promise.all(
      stateManager.state.players.map(fetchUsername),
    );
    gameRender.renderPlayerNames(names);
    WsConnectionManager.connect(stateManager.state.matchId);
    PlayerActionHandler.registerEventHandler();
  } catch (error) {
    console.error(error);
    gameRender.renderError("failed to setup game.");
  }
};

export const cleanupGame = () => {
  PlayerActionHandler.cleanup();
  WsConnectionManager.disconnect();
};
