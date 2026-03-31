import joblib
import numpy as np
import os
import warnings

# On cache les avertissements de version de XGBoost pour y voir plus clair
warnings.filterwarnings("ignore", category=UserWarning)

# Chemin absolu pour éviter les erreurs de dossier
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ressources", "model_xgboost_wins.pkl")

def get_best_move_ml(board):
    """
    Analyse chaque case vide et choisit celle qui MINIMISE 
    la probabilité de victoire de l'humain (X).
    """
    if not os.path.exists(MODEL_PATH):
        print(f"ATTENTION : Modèle introuvable. Mode Random.")
        import random
        empty = [i for i, c in enumerate(board) if c == ""]
        return random.choice(empty) if empty else None

    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Erreur chargement : {e}")
        return None

    empty_cells = [i for i, val in enumerate(board) if val == ""]
    best_move = None
    
    # --- CORRECTION ICI : Le nom de la variable doit être identique partout ---
    min_proba_val = float('inf') 

    for move_index in empty_cells:
        temp_board = list(board)
        temp_board[move_index] = "O"
        
        # Encodage 18 features
        features = []
        for cell in temp_board:
            features.append(1 if cell == "X" else 0)
            features.append(1 if cell == "O" else 0)
        
        input_data = np.array(features).reshape(1, -1)
        
        # Prédiction de la probabilité que X gagne
        # [0][1] correspond à la classe "1" (Victoire de X)
        proba_X_wins = model.predict_proba(input_data)[0][1]
        
        # On cherche le coup qui donne la probabilité la plus basse pour X
        if proba_X_wins < min_proba_val:
            min_proba_val = proba_X_wins
            best_move = move_index

    if best_move is not None:
        print(f"IA joue case {best_move} (Confiance victoire adverse : {min_proba_val:.2f})")
    
    return best_move