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

# ---------------------------------------------------------------------------
# 2. IA Minimax avec Alpha-Bêta
# ---------------------------------------------------------------------------

# Dictionnaire pour stocker les scores déjà calculés (Mémoïsation)
minimax_cache = {}

def get_minimax_score(board, is_x_turn, alpha=-2, beta=2):
    """
    Calcule le score optimal : +1 (X gagne), 0 (Nulle), -1 (O gagne)
    """
    state_key = (tuple(board), is_x_turn)
    if state_key in minimax_cache:
        return minimax_cache[state_key]

    winner = check_winner(board)
    if winner == 'X': return 1
    if winner == 'O': return -1
    if is_full(board): return 0

    if is_x_turn:
        best_score = -2
        for i in range(9):
            if board[i] is None:
                board[i] = 'X'
                score = get_minimax_score(board, False, alpha, beta)
                board[i] = None  # Backtracking
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha: break # Élagage Bêta
        minimax_cache[state_key] = best_score
        return best_score
    else:
        best_score = 2
        for i in range(9):
            if board[i] is None:
                board[i] = 'O'
                score = get_minimax_score(board, True, alpha, beta)
                board[i] = None
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha: break # Élagage Alpha
        minimax_cache[state_key] = best_score
        return best_score

# ---------------------------------------------------------------------------
# 3. Encodage et Préparation des données
# ---------------------------------------------------------------------------

def board_to_features(board):
    """ Transforme le plateau en 18 features binaires et calcule les cibles """
    # Encodage des 18 features (ci_x et ci_o)
    features = {}
    for i in range(9):
        features[f'c{i}_x'] = 1 if board[i] == 'X' else 0
        features[f'c{i}_o'] = 1 if board[i] == 'O' else 0

    # Calcul des cibles via Minimax
    # Note : Le dataset ne contient que les états où c'est au tour de X
    perfect_score = get_minimax_score(list(board), True)
    
    features['x_wins'] = 1 if perfect_score == 1 else 0
    features['is_draw'] = 1 if perfect_score == 0 else 0
    
    return features

# ---------------------------------------------------------------------------
# 4. Génération du Dataset (Parcours de l'arbre de jeu)
# ---------------------------------------------------------------------------

def generate_tic_tac_toe_dataset():
    
    all_data = []
    visited_states = set()
    
    # Pile pour le parcours : (plateau_en_tuple, tour_de_X)
    stack = [( (None,) * 9, True )]

    while stack:
        current_board, is_x_turn = stack.pop()
        
        # Éviter les doublons pour optimiser la génération
        if current_board in visited_states:
            continue
        visited_states.add(current_board)

        # On ne traite que les parties non terminées
        if check_winner(current_board) or is_full(current_board):
            continue

        # Si c'est au tour de X, on enregistre l'état dans le dataset
        if is_x_turn:
            row = board_to_features(current_board)
            all_data.append(row)

        # Ajouter les prochains coups possibles à la pile pour exploration
        current_player = 'X' if is_x_turn else 'O'
        for i in range(9):
            if current_board[i] is None:
                new_list = list(current_board)
                new_list[i] = current_player
                stack.append((tuple(new_list), not is_x_turn))

    # Conversion en DataFrame et export CSV
    df = pd.DataFrame(all_data)
    
    # S'assurer que le dossier ressources existe
    os.makedirs('ressources', exist_ok=True)
    df.to_csv('ressources/dataset.csv', index=False)
    
    print(f"Génération terminée : {len(df)} états uniques enregistrés dans ressources/dataset.csv")

generate_tic_tac_toe_dataset()