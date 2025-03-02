"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useUsername } from "./usernameContext";

export default function Home() {
  const { username, setUsername } = useUsername();
  const [error, setError] = useState("");
  const router = useRouter();

  const submitHandler = (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const matchId = e.target.matchId.value;
    if (!username || !matchId) {
      setError("user id or match id can not be empty.");
      return;
    }
    if (!Number.parseInt(username) || !Number.parseInt(matchId)) {
      setError("user id and match id have to be a number.");
      return;
    }
    setUsername(username);
    sessionStorage.setItem("username", username);
    router.push(`/game/${matchId}`);
  };
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <Link
        href="/match"
        style={{
          display: "inline-block",
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "#4CAF50",
          color: "white",
          borderRadius: "8px",
          textAlign: "center",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
          transition: "background-color 0.3s ease, transform 0.2s ease",
          textDecoration: "none", // デフォルトのリンクの下線を削除
        }}
      >
        <button
          type="button"
          style={{
            all: "unset",
            fontSize: "inherit",
            cursor: "pointer",
          }}
        >
          matchを作成
        </button>
      </Link>
      <h1>Gameをplay</h1>
      <h3>※まずはmatchを作成する必要があります</h3>
      <h3>match作成したplayer idとmatch idを以下に入力</h3>
      <form
        onSubmit={submitHandler}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "10px",
          maxWidth: "300px",
        }}
      >
        <div>
          <label
            htmlFor="username"
            style={{ display: "block", marginBottom: "5px" }}
          >
            Your user id
          </label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="1"
            style={{ width: "100%", padding: "8px", fontSize: "16px" }}
          />
        </div>
        <div>
          <label
            htmlFor="matchId"
            style={{ display: "block", marginBottom: "5px" }}
          >
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
        {error && <p style={{ color: "red" }}>{error}</p>} {/* エラー表示 */}
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
