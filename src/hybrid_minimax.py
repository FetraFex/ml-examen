"""
IA hybride : Minimax (profondeur max 3) + évaluation des feuilles par les modèles sklearn.

Plateau : liste de 9 entiers — 0 = vide, 1 = X, -1 = O.
Score feuille : proba_win * 1 + proba_draw * 0.5 (probas = classe 1 des deux LogisticRegression).
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import pandas as pd
from sklearn.linear_model import LogisticRegression

from .board_encoding import FEATURE_COLS, feature_row_to_dict

# Lignes gagnantes (indices 0..8)
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


def check_winner(board: List[int]) -> Optional[int]:
    """
    Retourne 1 si X gagne, -1 si O gagne, 0 si match nul (plateau plein),
    None si la partie continue.
    """
    for a, b, c in _WIN_LINES:
        if board[a] != 0 and board[a] == board[b] == board[c]:
            return board[a]
    if 0 not in board:
        return 0
    return None


def get_available_moves(board: List[int]) -> List[int]:
    """Indices des cases vides."""
    return [i for i in range(9) if board[i] == 0]


def make_move(board: List[int], move: int, player: int) -> List[int]:
    """
    `player` : 1 pour X, -1 pour O.
    Retourne un **nouveau** plateau (copie).
    """
    if board[move] != 0:
        raise ValueError("Case déjà occupée")
    if player not in (1, -1):
        raise ValueError("player doit être 1 (X) ou -1 (O)")
    b = list(board)
    b[move] = player
    return b


def encode_board(board: List[int]) -> List[int]:
    """
    Plateau 0 / 1 / -1 → 18 features binaires (c0_x, c0_o, …, c8_o).
    """
    if len(board) != 9:
        raise ValueError("Le plateau doit avoir 9 cases.")
    row: List[int] = []
    for v in board:
        if v == 0:
            row.extend([0, 0])
        elif v == 1:
            row.extend([1, 0])
        elif v == -1:
            row.extend([0, 1])
        else:
            raise ValueError("Valeur de case invalide (attendu 0, 1 ou -1).")
    return row


def _ml_score(
    board: List[int],
    model_xwins: LogisticRegression,
    model_draw: LogisticRegression,
) -> float:
    """score = P(x_wins=1) * 1 + P(is_draw=1) * 0.5"""
    row = encode_board(board)
    X = pd.DataFrame([feature_row_to_dict(row)])[FEATURE_COLS]
    proba_win = float(model_xwins.predict_proba(X)[0][1])
    proba_draw = float(model_draw.predict_proba(X)[0][1])
    return proba_win * 1.0 + proba_draw * 0.5


def minimax_hybride(
    board: List[int],
    depth: int,
    is_maximizing: bool,
    model_xwins: LogisticRegression,
    model_draw: LogisticRegression,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> float:
    """
    Minimax avec **élagage alpha-bêta**, profondeur max MAX_DEPTH (3).

    Feuille = profondeur >= 3 **ou** partie terminée → score ML (_ml_score).
    - is_maximizing=True : X **maximise** le score.
    - is_maximizing=False : O **minimise** le score.
    """
    w = check_winner(board)
    if w is not None or depth >= MAX_DEPTH:
        return _ml_score(board, model_xwins, model_draw)

    moves = get_available_moves(board)
    if not moves:
        return _ml_score(board, model_xwins, model_draw)

    if is_maximizing:
        best = float("-inf")
        for m in moves:
            child = make_move(board, m, 1)
            val = minimax_hybride(
                child, depth + 1, False, model_xwins, model_draw, alpha, beta
            )
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best

    best = float("inf")
    for m in moves:
        child = make_move(board, m, -1)
        val = minimax_hybride(
            child, depth + 1, True, model_xwins, model_draw, alpha, beta
        )
        best = min(best, val)
        beta = min(beta, best)
        if beta <= alpha:
            break
    return best


def current_player(board: List[int]) -> int:
    """1 si c'est au tour de X, -1 si c'est au tour de O (X commence)."""
    nx = sum(1 for x in board if x == 1)
    no = sum(1 for x in board if x == -1)
    return 1 if nx == no else -1


def get_best_move(
    board: List[int],
    model_xwins: LogisticRegression,
    model_draw: LogisticRegression,
) -> Optional[int]:
    """
    Choisit le meilleur coup pour le joueur dont c'est le tour,
    en explorant avec minimax_hybride depuis chaque coup légal.
    """
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
            val = minimax_hybride(child, 1, False, model_xwins, model_draw)
            if val > best_val:
                best_val = val
                best_move = m
    else:
        best_val = float("inf")
        for m in moves:
            child = make_move(board, m, -1)
            val = minimax_hybride(child, 1, True, model_xwins, model_draw)
            if val < best_val:
                best_val = val
                best_move = m

    return best_move


# --- Conversion pratique pour l’API (chaînes X / O / "") ---

def board_str_to_int(cells: List[str]) -> List[int]:
    m = {"": 0, "X": 1, "O": -1}
    out: List[int] = []
    for c in cells:
        if c not in m:
            raise ValueError("Case invalide")
        out.append(m[c])
    return out
