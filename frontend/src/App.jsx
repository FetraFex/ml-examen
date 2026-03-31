import { useCallback, useEffect, useState } from "react";

const empty = () => Array(9).fill("");

const WINS = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

function winner(board) {
  for (const [a, b, c] of WINS) {
    if (board[a] && board[a] === board[b] && board[b] === board[c]) return board[a];
  }
  return null;
}

function full(board) {
  return board.every(Boolean);
}

function cycleCell(cur) {
  if (cur === "") return "X";
  if (cur === "X") return "O";
  return "";
}

function PredictMetrics({ pred }) {
  if (!pred) return null;
  const px = Math.round(pred.p_x_wins_1 * 1000) / 10;
  const pd = Math.round(pred.p_is_draw_1 * 1000) / 10;
  return (
    <div className="predictions">
      <h3>Prédictions du modèle</h3>
      <div className="metric">
        <div className="metric-label">
          <span>X gagne (x_wins = 1)</span>
          <span className="metric-value">{px}%</span>
        </div>
        <div className="bar-track">
          <div className="bar-fill xwins" style={{ width: `${px}%` }} />
        </div>
        <div className="metric-sub">Complément : {(100 - px).toFixed(1)}% pour x_wins = 0</div>
      </div>
      <div className="metric">
        <div className="metric-label">
          <span>Match nul (is_draw = 1)</span>
          <span className="metric-value" style={{ color: "var(--warn)" }}>
            {pd}%
          </span>
        </div>
        <div className="bar-track">
          <div className="bar-fill draw" style={{ width: `${pd}%` }} />
        </div>
        <div className="metric-sub">Complément : {(100 - pd).toFixed(1)}% pour is_draw = 0</div>
      </div>
    </div>
  );
}

export default function App() {
  const [mode, setMode] = useState("test");
  const [apiOk, setApiOk] = useState(null);
  const [err, setErr] = useState(null);

  const [testBoard, setTestBoard] = useState(empty);
  const [pred, setPred] = useState(null);
  const [predLoading, setPredLoading] = useState(false);

  const [hvhBoard, setHvhBoard] = useState(empty);
  const [hvhTurn, setHvhTurn] = useState("X");

  const [hvmBoard, setHvmBoard] = useState(empty);
  const [humanIsX, setHumanIsX] = useState(true);
  const [hvmInit, setHvmInit] = useState(false);

  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then((d) => setApiOk(d.ok))
      .catch(() => setApiOk(false));
  }, []);

  const fetchPredict = useCallback(async (board) => {
    setErr(null);
    setPred(null);
    setPredLoading(true);
    try {
      const r = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board }),
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.detail || r.statusText);
      setPred(data);
    } catch (e) {
      setErr(String(e.message || e));
    } finally {
      setPredLoading(false);
    }
  }, []);

  const [aiVariant, setAiVariant] = useState("ml"); // "ml" | "hybrid"

  const fetchAiMove = useCallback(async (board, role) => {
    const r = await fetch("/api/ai-move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board, role }),
    });
    if (!r.ok) throw new Error("IA indisponible");
    const data = await r.json();
    return data.index;
  }, []);

  const fetchHybridMove = useCallback(async (board) => {
    const r = await fetch("/api/hybrid-move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board }),
    });
    if (!r.ok) throw new Error("IA hybride indisponible");
    const data = await r.json();
    return data.index;
  }, []);

  useEffect(() => {
    if (mode !== "hvm") return;
    const b = hvmBoard;
    if (!humanIsX && !b.some(Boolean) && !winner(b) && !hvmInit) {
      (async () => {
        try {
          const idx =
            aiVariant === "hybrid" ? await fetchHybridMove(b) : await fetchAiMove(b, "X");
          if (idx != null) {
            const nb = [...b];
            nb[idx] = "X";
            setHvmBoard(nb);
          }
          setHvmInit(true);
        } catch (e) {
          setErr(String(e.message || e));
        }
      })();
    }
  }, [mode, humanIsX, hvmBoard, hvmInit, fetchAiMove, fetchHybridMove, aiVariant]);

  const cycleTestCell = (i) => {
    const nb = [...testBoard];
    nb[i] = cycleCell(nb[i]);
    setTestBoard(nb);
    setPred(null);
  };

  const nx = hvmBoard.filter((c) => c === "X").length;
  const no = hvmBoard.filter((c) => c === "O").length;
  let humanTurnHvm = false;
  if (mode === "hvm") {
    const w = winner(hvmBoard);
    if (!w && !full(hvmBoard)) {
      humanTurnHvm = humanIsX ? nx === no : nx > no;
    }
  }

  const playHvm = async (idx) => {
    if (!humanTurnHvm || hvmBoard[idx]) return;
    const nb = [...hvmBoard];
    nb[idx] = humanIsX ? "X" : "O";
    setHvmBoard(nb);
    const w = winner(nb);
    const f = full(nb);
    if (w || f) return;
    try {
      const role = humanIsX ? "O" : "X";
      const ai =
        aiVariant === "hybrid" ? await fetchHybridMove(nb) : await fetchAiMove(nb, role);
      if (ai != null) {
        nb[ai] = role;
        setHvmBoard([...nb]);
      }
    } catch (e) {
      setErr(String(e.message || e));
    }
  };

  const wHvh = winner(hvhBoard);
  const wHvm = winner(hvmBoard);

  return (
    <div className="app">
      <header className="header">
        <h1>Morpion</h1>
        <div className={`api-badge ${apiOk === true ? "ok" : apiOk === false ? "bad" : ""}`}>
          <span className="dot" />
          {apiOk === null && "Connexion API…"}
          {apiOk === true && "API connectée · dataset chargé"}
          {apiOk === false && "API hors ligne — lance uvicorn (port 8000)"}
        </div>
      </header>

      {err && <div className="error">{err}</div>}

      <div className="card">
        <div className="mode-tabs">
          {[
            { id: "test", label: "Test ML" },
            { id: "hvh", label: "2 joueurs" },
            { id: "hvm", label: "vs IA" },
          ].map(({ id, label }) => (
            <button key={id} className={mode === id ? "active" : ""} type="button" onClick={() => setMode(id)}>
              {label}
            </button>
          ))}
        </div>

        {mode === "test" && (
          <>
            <p className="hint">Clique sur une case pour faire défiler : vide → X → O. Puis lance le calcul.</p>
            <div className="board-wrap">
              <div className="board">
                {testBoard.map((cell, i) => (
                  <button
                    key={i}
                    type="button"
                    className={`cell ${cell === "X" ? "x" : cell === "O" ? "o" : "empty-slot"}`}
                    onClick={() => cycleTestCell(i)}
                    title="Clic : vide → X → O"
                  >
                    {cell === "" ? "·" : cell}
                  </button>
                ))}
              </div>
            </div>
            <div className="actions">
              <button
                type="button"
                className="btn btn-primary"
                disabled={predLoading || apiOk === false}
                onClick={() => fetchPredict(testBoard)}
              >
                {predLoading ? "Calcul…" : "Calculer les probabilités"}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  setTestBoard(empty());
                  setPred(null);
                }}
              >
                Réinitialiser le plateau
              </button>
            </div>
            {predLoading && <p className="loading">Appel du modèle…</p>}
            <PredictMetrics pred={pred} />
          </>
        )}

        {mode === "hvh" && (
          <>
            <p className={`game-status ${wHvh ? "win" : full(hvhBoard) && !wHvh ? "draw" : ""}`}>
              {!wHvh && !full(hvhBoard) && `Tour des ${hvhTurn}`}
              {wHvh && `Victoire ${wHvh} !`}
              {full(hvhBoard) && !wHvh && "Match nul"}
            </p>
            <div className="board-wrap">
              <div className="board">
                {hvhBoard.map((cell, i) => (
                  <button
                    key={i}
                    type="button"
                    className={`cell ${cell === "X" ? "x" : cell === "O" ? "o" : ""}`}
                    disabled={!!cell || !!wHvh || full(hvhBoard)}
                    onClick={() => {
                      if (cell || wHvh || full(hvhBoard)) return;
                      const nb = [...hvhBoard];
                      nb[i] = hvhTurn;
                      setHvhBoard(nb);
                      setHvhTurn(hvhTurn === "X" ? "O" : "X");
                    }}
                  >
                    {cell || ""}
                  </button>
                ))}
              </div>
            </div>
            <div className="actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  setHvhBoard(empty());
                  setHvhTurn("X");
                }}
              >
                Nouvelle partie
              </button>
            </div>
          </>
        )}

        {mode === "hvm" && (
          <>
            <div className="toggle-row">
              <input
                type="checkbox"
                id="hx"
                checked={humanIsX}
                onChange={() => {
                  setHumanIsX(!humanIsX);
                  setHvmBoard(empty());
                  setHvmInit(false);
                }}
              />
              <label htmlFor="hx">Tu joues les X (sinon tu joues O, l’IA ouvre)</label>
            </div>
            <div className="toggle-row" style={{ flexWrap: "wrap", gap: "0.75rem" }}>
              <span style={{ color: "var(--muted)" }}>Stratégie IA :</span>
              <label>
                <input
                  type="radio"
                  name="aivar"
                  checked={aiVariant === "ml"}
                  onChange={() => {
                    setAiVariant("ml");
                    setHvmBoard(empty());
                    setHvmInit(false);
                  }}
                />{" "}
                ML seul
              </label>
              <label>
                <input
                  type="radio"
                  name="aivar"
                  checked={aiVariant === "hybrid"}
                  onChange={() => {
                    setAiVariant("hybrid");
                    setHvmBoard(empty());
                    setHvmInit(false);
                  }}
                />{" "}
                Hybride (Minimax 3 + ML)
              </label>
            </div>
            <p className={`game-status ${wHvm ? "win" : full(hvmBoard) && !wHvm ? "draw" : ""}`}>
              {!wHvm && !full(hvmBoard) && humanTurnHvm && "À toi de jouer"}
              {!wHvm && !full(hvmBoard) && !humanTurnHvm && "Tour de l’IA…"}
              {wHvm && `Victoire ${wHvm} !`}
              {full(hvmBoard) && !wHvm && "Match nul"}
            </p>
            <div className="board-wrap">
              <div className="board">
                {hvmBoard.map((cell, i) => (
                  <button
                    key={i}
                    type="button"
                    className={`cell ${cell === "X" ? "x" : cell === "O" ? "o" : ""}`}
                    disabled={!!cell || !!wHvm || full(hvmBoard) || !humanTurnHvm}
                    onClick={() => playHvm(i)}
                  >
                    {cell || ""}
                  </button>
                ))}
              </div>
            </div>
            <div className="actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  setHvmBoard(empty());
                  setHvmInit(false);
                }}
              >
                Nouvelle partie
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
