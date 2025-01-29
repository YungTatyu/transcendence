"use client";
import { useUsername } from "@/app/UsernameContext";
import { useParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";

const GAME_HEIGHT = 500;
const GAME_WIDTH = 800;
const BALL_WIDTH = 20;
const BALL_HEIGHT = 20;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;

const calcRemaingTime = (endTime) => {
  const now = Date.now(); // 現在時刻（ミリ秒）
  const re = Math.max(0, Math.floor((endTime - now) / 1000)); // 残り時間（秒単位）
  return re;
};

export default function Game() {
  const { matchId } = useParams();
  const { username: userid } = useUsername();
  const [gameState, setGameState] = useState({
    ball: { x: GAME_WIDTH / 2, y: GAME_HEIGHT / 2 },
    left_player: { id: "", y: GAME_HEIGHT / 2, score: 0 },
    right_player: { id: "", y: GAME_HEIGHT / 2, score: 0 },
  });
  const endTimeRef = useRef(0);
  const [remainingTime, setRemainingTime] = useState(0);
  const canvasRef = useRef(null);
  const socketRef = useRef(null);

  useEffect(() => {
    if (socketRef.current) {
      console.log("WebSocket is already connected");
      return; // WebSocketが既に存在する場合は再接続しない
    }
    const createWebSocketManager = (matchId) => {
      const REDIS_SERVER = "127.0.0.1:8001";
      const socket = new WebSocket(
        `ws://${REDIS_SERVER}/games/ws/enter-room/${matchId}/${userid}`,
      );

      const socketRef = socket;

      const startTimer = () => {
        const interval = setInterval(() => {
          const time = calcRemaingTime(endTimeRef.current);
          setRemainingTime(time);
          if (time <= 0) {
            clearInterval(interval);
          }
        }, 1000); // 1秒ごとに実行
      };

      socket.onopen = () => {
        console.log(`Connected to match: ${matchId}`);
      };

      socket.onmessage = (message) => {
        try {
          const parsedMessage = JSON.parse(message.data);

          if (
            parsedMessage.type === "game.message" &&
            parsedMessage.message === "update"
          ) {
            const updatedState = parsedMessage.data.state;

            setGameState({
              ball: updatedState.ball,
              left_player: updatedState.left_player,
              right_player: updatedState.right_player,
            });
          }
          if (
            parsedMessage.type === "game.message" &&
            parsedMessage.message === "timer"
          ) {
            endTimeRef.current = Number(parsedMessage.end_time) * 1000; // Unixタイム(秒) → ミリ秒に変換
            setRemainingTime(calcRemaingTime(endTimeRef.current));
            startTimer();
          }
        } catch (error) {
          console.error("Failed to parse WebSocket message:", error);
        }
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
    };

    const wsManager = createWebSocketManager(matchId);

    const registerEventHandler = (eventCallback) => {
      const upKey = "KeyW";
      const downKey = "KeyS";

      const handler = (e) => {
        if (e.code !== upKey && e.code !== downKey) {
          return;
        }
        const message = JSON.stringify({
          type: "game.paddle_move",
          key: e.code,
          userid: userid,
        });
        eventCallback(message);
      };

      document.addEventListener("keydown", handler);
      document.addEventListener("keyup", handler);

      // クリーンアップ時にイベントリスナーを削除
      return () => {
        document.removeEventListener("keydown", handler);
        document.removeEventListener("keyup", handler);
      };
    };

    const cleanupEventHandler = registerEventHandler(wsManager.sendMessage);

    // クリーンアップ処理
    return () => {
      wsManager.close();
      cleanupEventHandler();
    };
  }, [matchId, userid]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const draw = () => {
      // 背景クリア
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

      // ボールを球体として描画
      ctx.fillStyle = "white";
      ctx.beginPath();
      ctx.arc(
        gameState.ball.x + BALL_WIDTH / 2,
        gameState.ball.y + BALL_HEIGHT / 2,
        BALL_WIDTH / 2,
        0,
        Math.PI * 2,
      );
      ctx.fill();
      ctx.closePath();

      // 左プレイヤーのパドル描画
      ctx.fillStyle = "#0f0"; // 左プレイヤーのパドル色
      ctx.fillRect(0, gameState.left_player.y, PADDLE_WIDTH, PADDLE_HEIGHT);

      // 右プレイヤーのパドル描画
      ctx.fillStyle = "#f00"; // 右プレイヤーのパドル色
      ctx.fillRect(
        GAME_WIDTH - PADDLE_WIDTH,
        gameState.right_player.y,
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
      );

      // スコアとIDの描画
      ctx.fillStyle = "white";
      ctx.font = "24px Arial";
      // 左プレイヤーのIDとスコア
      ctx.fillText(`${gameState.left_player.id}`, 20, 30);
      ctx.font = "18px Arial"; // スコアのフォントサイズを少し小さく
      ctx.fillText(`${gameState.left_player.score}`, 20, 60);

      // 右プレイヤーのIDとスコア
      ctx.font = "24px Arial";
      ctx.fillText(`${gameState.right_player.id}`, GAME_WIDTH - 100, 30);
      ctx.font = "18px Arial";
      ctx.fillText(`${gameState.right_player.score}`, GAME_WIDTH - 100, 60);
    };

    draw();
  }, [gameState]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        backgroundColor: "#1e1e1e", // ダークテーマの背景色
        color: "white",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1
        style={{
          fontSize: "36px",
          marginBottom: "20px",
          fontWeight: "bold",
          textShadow: "2px 2px 10px rgba(0, 0, 0, 0.8)", // タイトルに影をつけて強調
        }}
      >
        Game Room: {matchId}
      </h1>
      <h2
        style={{
          fontSize: "24px",
          fontWeight: "bold",
          marginBottom: "10px",
          color: "#FFD700",
        }}
      >
        {remainingTime} sec
      </h2>

      <div
        style={{
          position: "relative",
          border: "2px solid white",
          boxShadow: "0 0 20px rgba(255, 255, 255, 0.5)", // キャンバスにシャドウを追加
          backgroundColor: "#000", // ゲームキャンバスの背景色を黒に
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <canvas
          ref={canvasRef}
          id="gameCanvas"
          width={GAME_WIDTH}
          height={GAME_HEIGHT}
          style={{
            border: "1px solid white",
            boxSizing: "border-box", // ボーダーをキャンバスサイズに含める
          }}
        />
      </div>
    </div>
  );
}
