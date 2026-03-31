"""
Encodage d'un plateau 3×3 vers les 18 features binaires du dataset.
Convention alignée sur baseline_logistic_regression.ipynb :
  c0_x, c0_o, c1_x, c1_o, …, c8_x, c8_o
"""

from __future__ import annotations

from typing import List, Literal, Sequence, Tuple

Cell = Literal["", "X", "O"]
Board = List[Cell]

FEATURE_COLS = [f"c{i}_{s}" for i in range(9) for s in ("x", "o")]


def board_to_feature_row(board: Sequence[Cell]) -> List[int]:
    """9 cases → liste de 18 entiers {0,1} dans l'ordre des colonnes CSV."""
    if len(board) != 9:
        raise ValueError("Le plateau doit avoir exactement 9 cases (indices 0..8).")
    out: List[int] = []
    for c in board:
        if c == "X":
            out.extend([1, 0])
        elif c == "O":
            out.extend([0, 1])
        elif c == "" or c is None:
            out.extend([0, 0])
        else:
            raise ValueError("Case invalide : utiliser '', 'X' ou 'O'.")
    return out


def feature_row_to_dict(row: Sequence[int]) -> dict:
    """18 valeurs → dict {nom_colonne: valeur} pour DataFrame / sklearn."""
    if len(row) != 18:
        raise ValueError("Attendu 18 features.")
    return dict(zip(FEATURE_COLS, row))


def empty_board() -> Board:
    return [""] * 9
