'use client'
import { useUsername } from "@/app/UsernameContext";
import { useParams } from "next/navigation"

const GAME_HEIGHT = 500;
const GAME_WIDTH = 800;
const BALL_WIDTH = 20;
const BALL_HEIGHT = 20;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;



export default function Game() {
  const { matchId } = useParams();
  const { userid } = useUsername();
  const [gameState, setGameState] = useState({
    ball: { x: 100, y: 200 },
    "": { y: 50, score: 0 },
    "": { y: 50, score: 0 },
  });

  const createWebSocketManager = (matchId) => {
    const REDIS_SERVER = "127.0.0.1:3000";
    const socket = new WebSocket(`ws://${REDIS_SERVER}/games/ws/enter-room/${matchId}`);

    socket.onopen = () => {
      console.log(`Connected to match: ${matchId}`);
    };

    socket.onmessage = (message) => {
      setGameState(message.data)
    };

    socket.onclose = () => {
      console.log("Disconnected from server");
    };

    socket.onerror = (error) => {
      console.log("WebSocket error:", error);
    };

    // メッセージ送信関数を返す
    return {
      sendMessage: (message) => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send(message);
        } else {
          console.log("Socket is not open. Unable to send message.");
        }
      },
      close: () => {
        socket.close();
      },
    };
  }

  const registerEventHandler = (eventCallback) => {
    const upKey = "WKey";
    const downKey = "SKey";

    const handler = (e) => {
      if (e.code !== upKey && e.code !== downKey) {
        return;
      }
      const message = JSON.stringify({
        type: "game.paddle_move", // メッセージのタイプ
        key: e.code,      // 押されたキー (例: "KeyW")
        username: userid,
      });
      eventCallback(message);
    }

    document.addEventListener('keydown', handler);
    document.addEventListener('keyup', handler);
  }

  const wsManager = createWebSocketManager(matchId);
  registerEventHandler(wsManager.sendMessage)

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const draw = () => {
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
        PADDLE_WIDTH,
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
    };

    draw();
  }, [gameState]);

  return (
    <div>
      <h1>Game Room: {matchId}</h1>
      <canvas
        ref={canvasRef}
        id="gameCanvas"
        width={GAME_WIDTH}
        height={GAME_HEIGHT}
        style={{ border: "1px solid white" }}
      ></canvas>
    </div>
  );
}
