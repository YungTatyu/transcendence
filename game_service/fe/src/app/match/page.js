"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Match() {
  const [error, setError] = useState("");
  const router = useRouter();

  const submitHandler = async (e) => {
    e.preventDefault();
    const matchId = e.target.matchId.value;
    const player1 = e.target.username1.value;
    const player2 = e.target.username2.value;
    if (!matchId || !player1 || !player2) {
      setError("match id or player fields cannot be empty.");
      return;
    }
    if (player1 === player2) {
      setError("player fields cannot be same.");
      return;
    }

    const response = await fetch("http://127.0.0.1:8001/games", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // データの形式を指定
      },
      body: JSON.stringify({
        matchId: matchId,
        userIdList: [player1, player2],
      }),
    });
    if (!response.ok) {
      const json = await response.json();
      console.error(json.error);
      alert(json.error);
    }
    router.push("/");
  };
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>matchを作成</h1>
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
            htmlFor="username1"
            style={{ display: "block", marginBottom: "5px" }}
          >
            player 1 id
          </label>
          <input
            type="text"
            id="username1"
            name="username1"
            placeholder="username1"
            style={{ width: "100%", padding: "8px", fontSize: "16px" }}
          />
        </div>
        <div>
          <label
            htmlFor="username2"
            style={{ display: "block", marginBottom: "5px" }}
          >
            player 2 id
          </label>
          <input
            type="text"
            id="username2"
            name="username2"
            placeholder="username2"
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
          Create a Match
        </button>
      </form>
    </div>
  );
}
