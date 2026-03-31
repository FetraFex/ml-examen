import numpy as np
import joblib
import os

# Chemins vers les futurs modèles (Step 2 & 3 du sujet)
MODEL_X_WINS = "models/model_x_wins.joblib"
MODEL_IS_DRAW = "models/model_is_draw.joblib"

def get_ml_features(board):
    """
    Transforme le plateau ['X', '', 'O'...] en vecteur de 18 features (Step 2.1)
    Ordre : [c0_x, c0_o, c1_x, c1_o, ..., c8_x, c8_o]
    """
    features = []
    for cell in board:
        features.append(1 if cell == "X" else 0) # ci_x
        features.append(1 if cell == "O" else 0) # ci_o
    return np.array(features).reshape(1, -1)

def get_best_move_ml(board):
    """
    Logique pour le mode 'vs IA (ML)'
    """
    # Si le fichier modèle n'existe pas encore, on joue au hasard
    if not os.path.exists(MODEL_X_WINS):
        import random
        empty = [i for i, c in enumerate(board) if c == ""]
        return random.choice(empty) if empty else None

    # TODO : Une fois le modèle entraîné par tes collègues :
    # 1. Charger le modèle : model = joblib.load(MODEL_X_WINS)
    # 2. Pour chaque case vide, simuler le coup et prédire la probabilité de victoire
    # 3. Retourner l'index de la case avec la proba la plus haute
    return None