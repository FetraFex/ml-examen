import { useState, useEffect, useCallback } from "react";

const WINNING_COMBOS = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

function checkWinner(board) {
  for (const [a, b, c] of WINNING_COMBOS) {
    if (board[a] && board[a] === board[b] && board[a] === board[c])
      return { winner: board[a], line: [a, b, c] };
  }
  return null;
}

const API_BASE_URL = "https://ml-examen-backend.onrender.com";

function boardToFeatures(board) {
  const features = new Array(18).fill(0);

  for (let i = 0; i < 9; i++) {
    if (board[i] === "X") {
      features[i] = 1;
    } else if (board[i] === "O") {
      features[i + 9] = 1;
    }
  }

  return features;
}

async function getAIMoveLogistic(board, aiPlayer = "O") {
  try {
    const features = boardToFeatures(board);

    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ features: features }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("API Error:", errorData);
      throw new Error(errorData.detail || "API request failed");
    }

    const result = await response.json();
    console.log("AI Prediction:", result);

    const available = board.reduce((arr, cell, idx) => {
      if (cell === null) arr.push(idx);
      return arr;
    }, []);

    if (available.length === 0) return null;

    let bestMove = null;
    let bestScore = aiPlayer === "O" ? Infinity : -Infinity;

    for (const move of available) {
      const testBoard = [...board];
      testBoard[move] = aiPlayer;

      const testFeatures = boardToFeatures(testBoard);
      const testResponse = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ features: testFeatures }),
      });

      if (testResponse.ok) {
        const testResult = await testResponse.json();

        if (aiPlayer === "O") {
          const score = testResult.win_probability;
          if (score < bestScore) {
            bestScore = score;
            bestMove = move;
          }
        } else {
          const score = testResult.win_probability;
          if (score > bestScore) {
            bestScore = score;
            bestMove = move;
          }
        }
      }
    }

    if (bestMove === null) {
      return getHeuristicMove(board, aiPlayer);
    }

    return bestMove;
  } catch (error) {
    console.error("AI API error, falling back to heuristic:", error);
    return getHeuristicMove(board, aiPlayer);
  }
}

function getHeuristicMove(board, aiPlayer) {
  const opponent = aiPlayer === "X" ? "O" : "X";
  const available = board.reduce((arr, cell, idx) => {
    if (cell === null) arr.push(idx);
    return arr;
  }, []);

  if (available.length === 0) return null;

  for (let move of available) {
    const testBoard = [...board];
    testBoard[move] = aiPlayer;
    if (checkWinner(testBoard)?.winner === aiPlayer) return move;
  }

  for (let move of available) {
    const testBoard = [...board];
    testBoard[move] = opponent;
    if (checkWinner(testBoard)?.winner === opponent) return move;
  }

  if (available.includes(4)) return 4;

  const corners = [0, 2, 6, 8].filter((c) => available.includes(c));
  if (corners.length)
    return corners[Math.floor(Math.random() * corners.length)];

  return available[Math.floor(Math.random() * available.length)];
}

async function getHybridMove(board, aiPlayer = "O") {
  try {
    const boardStrings = board.map(cell => cell === null ? "" : cell);
    
    const response = await fetch(`${API_BASE_URL}/hybrid-move`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ board: boardStrings }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Hybrid API Error:", errorData);
      throw new Error(errorData.detail || "Hybrid API request failed");
    }

    const result = await response.json();
    console.log("Hybrid AI Move:", result);
    
    if (result.move !== undefined && result.move !== -1) {
      return result.move;
    } else {
      console.log("No valid move from hybrid API, using heuristic");
      return getHeuristicMove(board, aiPlayer);
    }
    
  } catch (error) {
    console.error("Hybrid AI API error, falling back to heuristic:", error);
    return getHeuristicMove(board, aiPlayer);
  }
}

const MODES = [
  {
    id: "2p",
    label: "Two Players",
    tag: "LOCAL",
    desc: "Classic head-to-head on the same device. No AI, just brains.",
    icon: (
      <svg
        width="26"
        height="26"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="8" cy="7" r="3" />
        <circle cx="16" cy="7" r="3" />
        <path d="M2 21v-1a6 6 0 0 1 6-6h1" />
        <path d="M22 21v-1a6 6 0 0 0-6-6h-1" />
      </svg>
    ),
    cls: "two",
    badge: null,
    p2: "Player 2",
    aiFunction: null,
  },
  {
    id: "ia",
    label: "Vs IA",
    tag: "Machine Learning",
    desc: "Logistic regression trained on minimax game data. Calculated, statistical, beatable.",
    icon: (
      <svg
        width="26"
        height="26"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <rect x="2" y="9" width="20" height="12" rx="2" />
        <path d="M7 9V6a5 5 0 0 1 10 0v3" />
        <circle cx="12" cy="15" r="1.5" fill="currentColor" />
      </svg>
    ),
    cls: "ia",
    badge: "ML",
    p2: "IA",
    aiFunction: getAIMoveLogistic,
  },
  {
    id: "is",
    label: "Vs IS",
    tag: "Hybrid Engine",
    desc: "Minimax depth-3 with ML model evaluation at every node. Adaptive, ruthless, unpredictable.",
    icon: (
      <svg
        width="26"
        height="26"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
      </svg>
    ),
    cls: "is",
    badge: "HYBRID",
    p2: "IS",
    aiFunction: getHybridMove,
  },
];

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&display=swap');

  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --x-color: #ff4d6d;
    --o-color: #4cc9f0;
    --x-glow: rgba(255,77,109,0.35);
    --o-glow: rgba(76,201,240,0.35);
    --text: #e2e2f0;
    --muted: #4a4a6a;
    --accent: #7b5ea7;
    --win-bg: rgba(123,94,167,0.12);
    --two-color: #f4d03f;
    --ia-color: #4cc9f0;
    --is-color: #ff4d6d;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    font-family: 'DM Mono', monospace;
    color: var(--text);
    min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
  }

  .noise {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    opacity: 0.4;
  }

  .grid-bg {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
                      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 60px 60px; opacity: 0.3;
  }

  @keyframes fade-up {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .menu {
    position: relative; z-index: 1;
    display: flex; flex-direction: column; align-items: center; gap: 36px;
    padding: 56px 28px 48px;
    width: 100%; max-width: 500px;
    animation: fade-up 0.5s ease forwards;
  }

  .menu-header { text-align: center; }

  .menu-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(54px, 13vw, 84px);
    letter-spacing: 0.08em; line-height: 1;
    background: linear-gradient(135deg, var(--x-color) 0%, var(--accent) 50%, var(--o-color) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 0 36px rgba(123,94,167,0.55));
  }

  .menu-sub {
    font-size: 11px; letter-spacing: 0.32em;
    text-transform: uppercase; color: var(--muted); margin-top: 7px;
  }

  .section-label {
    font-size: 10px; letter-spacing: 0.3em;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: 12px; padding-left: 2px;
  }

  .mode-cards { display: flex; flex-direction: column; gap: 10px; width: 100%; }

  .mode-card {
    position: relative;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 18px; padding: 18px 20px;
    cursor: pointer; display: flex; align-items: center; gap: 16px;
    transition: border-color 0.25s, transform 0.18s, box-shadow 0.25s;
    overflow: hidden; text-align: left;
    opacity: 0; animation: fade-up 0.4s ease forwards;
  }

  .mode-card::before {
    content: '';
    position: absolute; inset: 0;
    opacity: 0; transition: opacity 0.3s; pointer-events: none;
  }

  .mode-card:hover { transform: translateX(5px); }
  .mode-card:hover::before { opacity: 1; }

  .mode-card.two:hover { border-color: rgba(244,208,63,0.5); box-shadow: -4px 0 0 0 rgba(244,208,63,0.5); }
  .mode-card.ia:hover  { border-color: rgba(76,201,240,0.5);  box-shadow: -4px 0 0 0 rgba(76,201,240,0.5); }
  .mode-card.is:hover  { border-color: rgba(255,77,109,0.5);  box-shadow: -4px 0 0 0 rgba(255,77,109,0.5); }

  .mode-card.two::before { background: linear-gradient(90deg, rgba(244,208,63,0.07) 0%, transparent 60%); }
  .mode-card.ia::before  { background: linear-gradient(90deg, rgba(76,201,240,0.07) 0%, transparent 60%); }
  .mode-card.is::before  { background: linear-gradient(90deg, rgba(255,77,109,0.07) 0%, transparent 60%); }

  .icon-box {
    width: 50px; height: 50px; flex-shrink: 0; border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    border: 1px solid var(--border); transition: border-color 0.25s, background 0.25s;
  }

  .mode-card.two .icon-box { color: var(--two-color); }
  .mode-card.ia  .icon-box { color: var(--ia-color); }
  .mode-card.is  .icon-box { color: var(--is-color); }

  .mode-card.two:hover .icon-box { border-color: rgba(244,208,63,0.35); background: rgba(244,208,63,0.08); }
  .mode-card.ia:hover  .icon-box { border-color: rgba(76,201,240,0.35);  background: rgba(76,201,240,0.08); }
  .mode-card.is:hover  .icon-box { border-color: rgba(255,77,109,0.35);  background: rgba(255,77,109,0.08); }

  .mode-info { flex: 1; min-width: 0; }

  .mode-name-row { display: flex; align-items: center; gap: 9px; margin-bottom: 4px; }

  .mode-name {
    font-family: 'Bebas Neue', sans-serif; font-size: 22px;
    letter-spacing: 0.06em; line-height: 1;
  }

  .mode-card.two .mode-name { color: var(--two-color); }
  .mode-card.ia  .mode-name { color: var(--ia-color); }
  .mode-card.is  .mode-name { color: var(--is-color); }

  .mode-tag {
    font-size: 9px; letter-spacing: 0.18em; text-transform: uppercase;
    padding: 3px 8px; border-radius: 100px; border: 1px solid transparent;
  }

  .mode-card.two .mode-tag { color: var(--two-color); border-color: rgba(244,208,63,0.28); background: rgba(244,208,63,0.07); }
  .mode-card.ia  .mode-tag { color: var(--ia-color);  border-color: rgba(76,201,240,0.28);  background: rgba(76,201,240,0.07); }
  .mode-card.is  .mode-tag { color: var(--is-color);  border-color: rgba(255,77,109,0.28);  background: rgba(255,77,109,0.07); }

  .mode-desc { font-size: 11px; color: var(--muted); line-height: 1.65; }

  .mode-badge {
    flex-shrink: 0;
    font-family: 'Bebas Neue', sans-serif; font-size: 11px; letter-spacing: 0.12em;
    padding: 5px 9px; border-radius: 8px; border: 1px solid; line-height: 1;
  }

  .mode-card.ia .mode-badge { color: var(--ia-color); border-color: rgba(76,201,240,0.22); background: rgba(76,201,240,0.06); }
  .mode-card.is .mode-badge { color: var(--is-color); border-color: rgba(255,77,109,0.22); background: rgba(255,77,109,0.06); }

  .mode-arrow { color: var(--muted); flex-shrink: 0; transition: transform 0.22s, color 0.22s; }
  .mode-card:hover .mode-arrow { transform: translateX(4px); color: var(--text); }

  .menu-footer {
    font-size: 10px; letter-spacing: 0.15em;
    text-transform: uppercase; color: var(--muted); opacity: 0.45;
  }

  .game {
    position: relative; z-index: 1;
    display: flex; flex-direction: column; align-items: center; gap: 26px;
    padding: 36px 28px 48px;
    width: 100%; max-width: 480px;
    animation: fade-up 0.4s ease forwards;
  }

  .game-top { width: 100%; display: flex; align-items: flex-start; gap: 12px; }

  .btn-back {
    background: transparent; border: 1px solid var(--border);
    color: var(--muted); border-radius: 10px;
    width: 38px; height: 38px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.2s; margin-top: 3px;
  }

  .btn-back:hover { border-color: var(--accent); color: var(--text); background: rgba(123,94,167,0.1); }

  .game-header { flex: 1; }

  .title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(38px, 9vw, 58px);
    letter-spacing: 0.08em; line-height: 1;
    background: linear-gradient(135deg, var(--x-color) 0%, var(--accent) 50%, var(--o-color) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 0 20px rgba(123,94,167,0.45));
  }

  .mode-pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase;
    padding: 4px 10px; border-radius: 100px; border: 1px solid; margin-top: 5px;
  }
  .mode-pill-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }

  .mode-pill.two { color: var(--two-color); border-color: rgba(244,208,63,0.3);  background: rgba(244,208,63,0.07); }
  .mode-pill.ia  { color: var(--ia-color);  border-color: rgba(76,201,240,0.3);  background: rgba(76,201,240,0.07); }
  .mode-pill.is  { color: var(--is-color);  border-color: rgba(255,77,109,0.3);  background: rgba(255,77,109,0.07); }

  .scoreboard {
    display: flex; gap: 8px; align-items: center;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 12px 20px; width: 100%;
  }

  .score-player { flex: 1; text-align: center; display: flex; flex-direction: column; gap: 4px; }

  .score-label { font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase; color: var(--muted); }
  .score-label.x { color: var(--x-color); }
  .score-label.o { color: var(--o-color); }

  .score-num { font-family: 'Bebas Neue', sans-serif; font-size: 36px; line-height: 1; }
  .score-num.x     { color: var(--x-color); text-shadow: 0 0 20px var(--x-glow); }
  .score-num.o     { color: var(--o-color); text-shadow: 0 0 20px var(--o-glow); }
  .score-num.draws { color: var(--muted); }

  .score-divider { width: 1px; height: 40px; background: var(--border); }

  .status-bar {
    height: 44px; display: flex; align-items: center; justify-content: center;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 0 24px; width: 100%;
    transition: border-color 0.3s;
  }

  .status-bar.x-turn { border-color: rgba(255,77,109,0.35); }
  .status-bar.o-turn { border-color: rgba(76,201,240,0.35); }
  .status-bar.win    { border-color: var(--accent); background: var(--win-bg); }
  .status-bar.draw   { border-color: var(--muted); }

  .status-text { font-size: 13px; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 500; }

  .marker {
    display: inline-block;
    font-family: 'Bebas Neue', sans-serif; font-size: 18px; margin: 0 6px;
    animation: blink 1s ease-in-out infinite;
  }
  .marker.x { color: var(--x-color); text-shadow: 0 0 12px var(--x-glow); }
  .marker.o { color: var(--o-color); text-shadow: 0 0 12px var(--o-glow); }

  @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

  .board-wrap { position: relative; width: 100%; aspect-ratio: 1; max-width: 360px; }

  .board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; }

  .cell {
    aspect-ratio: 1;
    background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; position: relative; overflow: hidden;
    transition: border-color 0.25s, background 0.25s, transform 0.15s;
  }
  .cell:hover:not(.filled):not(.disabled) {
    border-color: var(--accent); background: rgba(123,94,167,0.08); transform: scale(1.02);
  }
  .cell.filled   { cursor: default; }
  .cell.disabled { cursor: not-allowed; }
  .cell.win-cell {
    border-color: rgba(123,94,167,0.6); background: var(--win-bg);
    animation: win-pulse 1s ease-in-out infinite;
  }

  @keyframes win-pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(123,94,167,0); }
    50%      { box-shadow: 0 0 0 4px rgba(123,94,167,0.2); }
  }

  .cell-ripple {
    position: absolute; inset: 0; border-radius: 16px;
    animation: ripple 0.4s ease-out forwards; pointer-events: none;
  }
  .cell-ripple.x { background: radial-gradient(circle, var(--x-glow) 0%, transparent 70%); }
  .cell-ripple.o { background: radial-gradient(circle, var(--o-glow) 0%, transparent 70%); }

  @keyframes ripple {
    from { opacity:1; transform: scale(0); }
    to   { opacity:0; transform: scale(2.5); }
  }

  .symbol {
    width: 52%; height: 52%;
    animation: pop-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  }
  @keyframes pop-in {
    from { opacity:0; transform: scale(0.3) rotate(-15deg); }
    to   { opacity:1; transform: scale(1) rotate(0deg); }
  }

  .btn-ghost {
    background: transparent; border: 1px solid var(--border);
    color: var(--muted); font-family: 'DM Mono', monospace;
    font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase;
    padding: 11px 24px; border-radius: 100px; cursor: pointer;
    transition: all 0.25s; display: flex; align-items: center; gap: 8px;
  }
  .btn-ghost:hover { border-color: var(--accent); color: var(--text); background: rgba(123,94,167,0.1); }
  .btn-ghost svg { transition: transform 0.5s; }
  .btn-ghost:hover svg { transform: rotate(180deg); }
`;

function XSymbol() {
  return (
    <svg
      viewBox="0 0 60 60"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="symbol"
    >
      <line
        x1="10"
        y1="10"
        x2="50"
        y2="50"
        stroke="var(--x-color)"
        strokeWidth="7"
        strokeLinecap="round"
      />
      <line
        x1="50"
        y1="10"
        x2="10"
        y2="50"
        stroke="var(--x-color)"
        strokeWidth="7"
        strokeLinecap="round"
      />
      <line
        x1="10"
        y1="10"
        x2="50"
        y2="50"
        stroke="var(--x-color)"
        strokeWidth="14"
        strokeLinecap="round"
        opacity="0.13"
      />
      <line
        x1="50"
        y1="10"
        x2="10"
        y2="50"
        stroke="var(--x-color)"
        strokeWidth="14"
        strokeLinecap="round"
        opacity="0.13"
      />
    </svg>
  );
}

function OSymbol() {
  return (
    <svg
      viewBox="0 0 60 60"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="symbol"
    >
      <circle cx="30" cy="30" r="18" stroke="var(--o-color)" strokeWidth="7" />
      <circle
        cx="30"
        cy="30"
        r="18"
        stroke="var(--o-color)"
        strokeWidth="14"
        opacity="0.13"
      />
    </svg>
  );
}

function ModeMenu({ onSelect }) {
  return (
    <>
      <style>{css}</style>
      <div className="noise" />
      <div className="grid-bg" />
      <div className="menu">
        <div className="menu-header">
          <div className="menu-title">TIC TAC TOE</div>
          <div className="menu-sub">choose your game mode</div>
        </div>

        <div style={{ width: "100%" }}>
          <div className="section-label">select mode</div>
          <div className="mode-cards">
            {MODES.map((m, i) => (
              <button
                key={m.id}
                className={`mode-card ${m.cls}`}
                style={{ animationDelay: `${0.1 + i * 0.08}s` }}
                onClick={() => onSelect(m.id)}
              >
                <div className="icon-box">{m.icon}</div>

                <div className="mode-info">
                  <div className="mode-name-row">
                    <span className="mode-name">{m.label}</span>
                    <span className="mode-tag">{m.tag}</span>
                  </div>
                  <div className="mode-desc">{m.desc}</div>
                </div>

                {m.badge && <div className="mode-badge">{m.badge}</div>}

                <svg
                  className="mode-arrow"
                  width="15"
                  height="15"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </button>
            ))}
          </div>
        </div>

        <div className="menu-footer">v2.0 · select a mode to begin</div>
      </div>
    </>
  );
}

function GameBoard({ mode, onBack }) {
  const meta = MODES.find((m) => m.id === mode);
  const aiFunction = meta?.aiFunction;

  const [board, setBoard] = useState(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState(true);
  const [scores, setScores] = useState({ X: 0, O: 0, D: 0 });
  const [ripple, setRipple] = useState({ idx: -1, key: 0 });
  const [isAIThinking, setIsAIThinking] = useState(false);
  const [apiError, setApiError] = useState(null);

  const result = checkWinner(board);
  const isDraw = !result && board.every(Boolean);
  const gameOver = !!result || isDraw;

  useEffect(() => {
    if (result) {
      setScores((s) => ({ ...s, [result.winner]: s[result.winner] + 1 }));
    } else if (isDraw) {
      setScores((s) => ({ ...s, D: s.D + 1 }));
    }
  }, [result?.winner, isDraw]);

  useEffect(() => {
    const isAITurn = () => {
      if (gameOver) return false;
      if (mode === "2p") return false;
      const currentPlayer = xIsNext ? "X" : "O";
      return currentPlayer === "O";
    };

    if (isAITurn() && !isAIThinking && aiFunction) {
      const makeAIMove = async () => {
        setIsAIThinking(true);
        setApiError(null);
        try {
          const move = await aiFunction(board, "O");
          if (
            move !== null &&
            move !== undefined &&
            !board[move] &&
            !gameOver
          ) {
            const newBoard = [...board];
            newBoard[move] = "O";
            setBoard(newBoard);
            setXIsNext(true);
            setRipple({ idx: move, key: Date.now() });
          }
        } catch (error) {
          console.error("AI move error:", error);
          setApiError("AI error, using fallback");
        } finally {
          setIsAIThinking(false);
        }
      };

      const timeoutId = setTimeout(() => {
        makeAIMove();
      }, 300);

      return () => clearTimeout(timeoutId);
    }
  }, [board, xIsNext, gameOver, mode, aiFunction, isAIThinking]);

  const handleClick = async (idx) => {
    if (board[idx] || gameOver) return;
    if (mode !== "2p" && !xIsNext) return;
    if (isAIThinking) return;

    const newBoard = [...board];
    newBoard[idx] = xIsNext ? "X" : "O";
    setBoard(newBoard);
    setXIsNext(p => !p);      
    setRipple({ idx, key: Date.now() });
  };

  const reset = () => {
    setBoard(Array(9).fill(null));
    setXIsNext(true);
    setIsAIThinking(false);
    setApiError(null);
  };

  const currentPlayer = xIsNext ? "X" : "O";
  const winLine = result?.line ?? [];

  const playerLabel = (sym) =>
    sym === "O" && mode !== "2p" ? meta.p2 : `P${sym === "X" ? 1 : 2}`;

  let statusContent;
  if (result) {
    statusContent = (
      <span className="status-text">
        <span className={`marker ${result.winner.toLowerCase()}`}>
          {result.winner}
        </span>
        {playerLabel(result.winner)} wins
      </span>
    );
  } else if (isDraw) {
    statusContent = (
      <span className="status-text" style={{ color: "var(--muted)" }}>
        draw — no winners
      </span>
    );
  } else if (mode !== "2p" && !xIsNext && !gameOver) {
    statusContent = (
      <span className="status-text">
        {isAIThinking ? "AI thinking..." : "AI is calculating..."}
      </span>
    );
  } else {
    statusContent = (
      <span className="status-text">
        <span className={`marker ${currentPlayer.toLowerCase()}`}>
          {currentPlayer}
        </span>
        {playerLabel(currentPlayer)}'s turn
      </span>
    );
  }

  const statusClass = result
    ? "win"
    : isDraw
    ? "draw"
    : xIsNext
    ? "x-turn"
    : "o-turn";

  return (
    <>
      <style>{css}</style>
      <div className="noise" />
      <div className="grid-bg" />
      <div className="game">
        <div className="game-top">
          <button className="btn-back" onClick={onBack} title="Back to menu">
            <svg
              width="15"
              height="15"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M19 12H5M12 5l-7 7 7 7" />
            </svg>
          </button>
          <div className="game-header">
            <div className="title">TIC TAC TOE</div>
            <div className={`mode-pill ${meta.cls}`}>
              <span className="mode-pill-dot" />
              {meta.label} · {meta.tag}
            </div>
          </div>
        </div>

        <div className="scoreboard">
          <div className="score-player">
            <span className="score-label x">X · P1</span>
            <span className="score-num x">{scores.X}</span>
          </div>
          <div className="score-divider" />
          <div className="score-player">
            <span className="score-label">draws</span>
            <span className="score-num draws">{scores.D}</span>
          </div>
          <div className="score-divider" />
          <div className="score-player">
            <span className="score-label o">O · {meta.p2}</span>
            <span className="score-num o">{scores.O}</span>
          </div>
        </div>

        <div className={`status-bar ${statusClass}`}>
          {statusContent}
          {apiError && (
            <span
              style={{
                marginLeft: "8px",
                fontSize: "9px",
                color: "var(--is-color)",
              }}
            >
              ({apiError})
            </span>
          )}
        </div>

        <div className="board-wrap">
          <div className="board">
            {board.map((cell, i) => {
              const isWin = winLine.includes(i);
              return (
                <div
                  key={i}
                  className={[
                    "cell",
                    cell ? "filled" : "",
                    gameOver && !cell ? "disabled" : "",
                    isWin ? "win-cell" : "",
                    isAIThinking && !xIsNext && !gameOver && !cell
                      ? "disabled"
                      : "",
                  ].join(" ")}
                  onClick={() => handleClick(i)}
                >
                  {ripple.idx === i && cell && (
                    <div
                      key={ripple.key}
                      className={`cell-ripple ${cell.toLowerCase()}`}
                    />
                  )}
                  {cell === "X" && <XSymbol />}
                  {cell === "O" && <OSymbol />}
                </div>
              );
            })}
          </div>
        </div>

        <button className="btn-ghost" onClick={reset}>
          <svg
            width="13"
            height="13"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
            <path d="M3 3v5h5" />
          </svg>
          new round
        </button>
      </div>
    </>
  );
}

export default function App() {
  const [mode, setMode] = useState(null);
  if (!mode) return <ModeMenu onSelect={setMode} />;
  return <GameBoard mode={mode} onBack={() => setMode(null)} />;
}