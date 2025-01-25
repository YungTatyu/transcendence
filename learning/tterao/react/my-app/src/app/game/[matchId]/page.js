'use client'
import { useParams } from "next/navigation"

export default function Game() {
  const { matchId } = useParams();
  return <div>
    game
    <div>{matchId}</div>
  </div>
}
