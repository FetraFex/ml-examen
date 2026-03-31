import os
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Logique de Jeu (Tic-Tac-Toe)
# ---------------------------------------------------------------------------

# 8 lignes gagnantes possibles sur un plateau 3x3
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Lignes
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colonnes
    (0, 4, 8), (2, 4, 6),             # Diagonales
]

def check_winner(board):
    """ Retourne 'X', 'O' ou None """
    for a, b, c in WINNING_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board):
    """ Retourne True si le plateau est rempli """
    return all(cell is not None for cell in board)
