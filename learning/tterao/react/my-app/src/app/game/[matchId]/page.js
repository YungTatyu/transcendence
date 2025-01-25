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
      if (!keys.hasOwnProperty(e.code)) {
        return;
      }
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

  return <div>
    game
    <div>{matchId}</div>
  </div>
}
