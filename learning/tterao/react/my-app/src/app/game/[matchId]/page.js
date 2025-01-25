'use client'
import { useUsername } from "@/app/UsernameContext";
import { useParams } from "next/navigation"

export function connectToWebSocket(matchId) {
  const REDIS_SERVER = "127.0.0.1:3000"
  const socket = new WebSocket(`ws://${REDIS_SERVER}/games/ws/enter-room/${matchId}`);

  socket.onopen = () => {
    console.log(`Connected to match: ${matchId}`);
  };

  socket.onmessage = (message) => {
    console.log('Message from server:', message.data);
  };

  socket.onclose = () => {
    console.log('Disconnected from server');
  };

  socket.onerror = () => {
    console.log('error');
  };

  return socket;
}

export default function Game() {
  const { matchId } = useParams();
  const { userid } = useUsername()
  return <div>
    game
    <div>{matchId}</div>
  </div>
}
