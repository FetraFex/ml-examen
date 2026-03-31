from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Tuple

# Initialisation de l'application
app = FastAPI(title="Morpion Logistic Regression API")

# Configuration CORS pour React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle de régression logistique
MODEL_PATH = "models/tic_tac_toe_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print(f"Modèle chargé avec succès : {MODEL_PATH}")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None

# Constantes pour le minimax
_WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)
MAX_DEPTH = 3


# Schéma de données attendu en entrée (les 18 colonnes binaires)
class GameState(BaseModel):
    features: list


class HybridMoveRequest(BaseModel):
    board: List[str]


class MoveResponse(BaseModel):
    move: int
    board: List[str]
    score: Optional[float] = None
    message: str


# Fonctions utilitaires pour le minimax
def board_str_to_int(cells: List[str]) -> List[int]:
    mapping = {"": 0, "X": 1, "O": -1}
    return [mapping.get(c, 0) for c in cells]


def board_int_to_str(board: List[int]) -> List[str]:
    mapping = {0: "", 1: "X", -1: "O"}
    return [mapping.get(v, "") for v in board]


def check_winner(board: List[int]) -> Optional[int]:
    for a, b, c in _WIN_LINES:
        if board[a] != 0 and board[a] == board[b] == board[c]:
            return board[a]
    if 0 not in board:
        return 0
    return None


def get_available_moves(board: List[int]) -> List[int]:
    return [i for i in range(9) if board[i] == 0]


def make_move(board: List[int], move: int, player: int) -> List[int]:
    if board[move] != 0:
        raise ValueError("Cell already occupied")
    b = list(board)
    b[move] = player
    return b


def current_player(board: List[int]) -> int:
    nx = sum(1 for x in board if x == 1)
    no = sum(1 for x in board if x == -1)
    return 1 if nx == no else -1


def encode_board(board: List[int]) -> List[int]:
    if len(board) != 9:
        raise ValueError("Board must have 9 cells")
    row: List[int] = []
    for v in board:
        if v == 0:
            row.extend([0, 0])
        elif v == 1:
            row.extend([1, 0])
        elif v == -1:
            row.extend([0, 1])
        else:
            raise ValueError("Invalid cell value")
    return row


def evaluate_board_with_ml(board: List[int], model_xwins) -> float:
    winner = check_winner(board)
    if winner == 1:
        return 1.0
    elif winner == -1:
        return 0.0
    elif winner == 0:
        return 0.5

    try:
        row = encode_board(board)
        input_data = np.array(row).reshape(1, -1)
        proba_win = float(model_xwins.predict_proba(input_data)[0][1])
        return proba_win
    except Exception as e:
        print(f"ML evaluation error: {e}")
        return 0.5


def minimax_hybride(
    board: List[int],
    depth: int,
    is_maximizing: bool,
    model_xwins,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> float:
    winner = check_winner(board)

    if winner is not None:
        if winner == 1:
            return 1.0
        elif winner == -1:
            return 0.0
        else:
            return 0.5

    if depth >= MAX_DEPTH:
        return evaluate_board_with_ml(board, model_xwins)

    moves = get_available_moves(board)
    if not moves:
        return evaluate_board_with_ml(board, model_xwins)

    if is_maximizing:
        best = float("-inf")
        for m in moves:
            child = make_move(board, m, 1)
            val = minimax_hybride(child, depth + 1, False, model_xwins, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best

    best = float("inf")
    for m in moves:
        child = make_move(board, m, -1)
        val = minimax_hybride(child, depth + 1, True, model_xwins, alpha, beta)
        best = min(best, val)
        beta = min(beta, best)
        if beta <= alpha:
            break
    return best


def get_best_move(board: List[int], model_xwins) -> Optional[int]:
    if check_winner(board) is not None:
        return None

    moves = get_available_moves(board)
    if not moves:
        return None

    player = current_player(board)
    best_move: Optional[int] = None

    if player == 1:
        best_val = float("-inf")
        for m in moves:
            child = make_move(board, m, 1)
            val = minimax_hybride(child, 1, False, model_xwins)
            if val > best_val:
                best_val = val
                best_move = m
    else:
        best_val = float("inf")
        for m in moves:
            child = make_move(board, m, -1)
            val = minimax_hybride(child, 1, True, model_xwins)
            if val < best_val:
                best_val = val
                best_move = m

    return best_move


# Endpoints existants
@app.get("/")
def health_check():
    return {"status": "online", "model": "LogisticRegression"}


@app.post("/predict")
async def predict(data: GameState):
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé sur le serveur")

    if len(data.features) != 18:
        raise HTTPException(
            status_code=400, detail="Le modèle attend exactement 18 caractéristiques"
        )

    try:
        input_data = np.array(data.features).reshape(1, -1)
        probabilities = model.predict_proba(input_data)
        win_probability = float(probabilities[0][1])
        prediction = int(model.predict(input_data)[0])

        return {
            "win_probability": round(win_probability, 4),
            "prediction": prediction,
            "message": (
                "Victoire probable de X"
                if prediction == 1
                else "Pas de victoire détectée"
            ),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Nouvel endpoint pour le mode hybride
@app.post("/hybrid-move", response_model=MoveResponse)
async def hybrid_move(request: HybridMoveRequest):
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Modèle non chargé. Impossible d'exécuter le mode hybride.",
        )

    try:
        board_int = board_str_to_int(request.board)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Plateau invalide: {str(e)}")

    if len(board_int) != 9:
        raise HTTPException(status_code=400, detail="Le plateau doit avoir 9 cases")

    winner = check_winner(board_int)
    if winner is not None:
        if winner == 0:
            return MoveResponse(
                move=-1, board=request.board, message="Match nul - partie terminée"
            )
        else:
            winner_str = "X" if winner == 1 else "O"
            return MoveResponse(
                move=-1,
                board=request.board,
                message=f"Partie terminée - {winner_str} a gagné",
            )

    moves = get_available_moves(board_int)
    if not moves:
        return MoveResponse(
            move=-1, board=request.board, message="Plus de coups disponibles"
        )

    try:
        best_move = get_best_move(board_int, model)

        if best_move is None:
            best_move = moves[0]

        player = current_player(board_int)
        new_board_int = make_move(board_int, best_move, player)
        new_board_str = board_int_to_str(new_board_int)

        position_score = evaluate_board_with_ml(new_board_int, model)

        player_str = "X" if player == 1 else "O"

        return MoveResponse(
            move=best_move,
            board=new_board_str,
            score=round(position_score, 4),
            message=f"IA ({player_str}) joue case {best_move} (score position: {round(position_score, 4)})",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du calcul du coup: {str(e)}"
        )


@app.post("/evaluate")
async def evaluate_position(request: HybridMoveRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")

    try:
        board_int = board_str_to_int(request.board)
        score = evaluate_board_with_ml(board_int, model)
        winner = check_winner(board_int)

        return {
            "score": round(score, 4),
            "winner": (
                winner
                if winner is None
                else ("X" if winner == 1 else "O" if winner == -1 else "draw")
            ),
            "is_terminal": winner is not None,
            "moves_available": len(get_available_moves(board_int)),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="https://ml-examen.vercel.app/", port=8000)
