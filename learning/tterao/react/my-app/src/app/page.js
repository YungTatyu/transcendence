'use client'
import Image from "next/image";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";
import { useUsername } from "./UsernameContext";
import { useState } from "react";

export default function Home() {
  const { username, setUsername } = useUsername();
  const [error, setError] = useState('');
  const router = useRouter()

  const submitHandler = (e) => {
    e.preventDefault()
    const username = e.target.username.value;
    const matchId = e.target.matchId.value;
    if (!username || !matchId) {
      setError("username or match id can not be empty.")
      return
    }
    setUsername(username);
    router.push(`/game`)
  }
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>ユーザーネームを入力してください</h1>
      <form onSubmit={submitHandler} style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "300px" }}>
        <div>
          <label htmlFor="username" style={{ display: "block", marginBottom: "5px" }}>
            ユーザーネーム
          </label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="username"
            style={{ width: "100%", padding: "8px", fontSize: "16px" }}
          />
        </div>
        <div>
          <label htmlFor="matchId" style={{ display: "block", marginBottom: "5px" }}>
            match id
          </label>
          <input
            type="text"
            id="matchId"
            name="matchId"
            placeholder="1"
            style={{ width: "100%", padding: "8px", fontSize: "16px" }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>} {/* エラー表示 */}
        <button
          type="submit"
          style={{
            padding: "10px",
            fontSize: "16px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}

        >
          Go to Game
        </button>
      </form>
    </div>
  );
}
