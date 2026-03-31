"""
Baseline LogisticRegression : même logique que baseline_logistic_regression.ipynb
(hyperparamètres identiques), utilisable par l'interface sans importer le notebook.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from .board_encoding import FEATURE_COLS, board_to_feature_row, feature_row_to_dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "ressources" / "dataset2.csv"

TARGET_X_WINS = "x_wins"
TARGET_IS_DRAW = "is_draw"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_dataset(csv_path: Optional[Path] = None) -> pd.DataFrame:
    path = csv_path or DEFAULT_DATA_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Dataset introuvable : {path}")
    return pd.read_csv(path)


def train_baseline_models(
    df: pd.DataFrame,
) -> Tuple[LogisticRegression, LogisticRegression, Dict[str, Any]]:
    """Entraîne les deux modèles sur tout le dataframe (pour l'interface / démo)."""
    X = df[FEATURE_COLS]
    y_x = df[TARGET_X_WINS]
    y_d = df[TARGET_IS_DRAW]

    # Même split aligné que dans le notebook (pour cohérence si on veut des métriques)
    X_train, _, yx_train, _, yd_train, _ = train_test_split(
        X,
        y_x,
        y_d,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y_x,
    )

    m_x = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    m_d = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    m_x.fit(X_train, yx_train)
    m_d.fit(X_train, yd_train)

    meta = {
        "n_samples": len(df),
        "n_train": len(X_train),
        "path": str(DEFAULT_DATA_PATH),
    }
    return m_x, m_d, meta


def predict_proba_for_row(
    model_x: LogisticRegression,
    model_d: LogisticRegression,
    feature_row: List[int],
) -> Tuple[float, float, float, float]:
    """
    Retourne (p_x_wins classe 1, p_x_wins classe 0, p_draw classe 1, p_draw classe 0).
    Ordre sklearn : colonne 0 = classe 0, colonne 1 = classe 1.
    """
    X = pd.DataFrame([feature_row_to_dict(feature_row)])[FEATURE_COLS]
    px = model_x.predict_proba(X)[0]
    pd_ = model_d.predict_proba(X)[0]
    # binaire : [P(0), P(1)]
    return float(px[1]), float(px[0]), float(pd_[1]), float(pd_[0])


def _combined_ml_score(
    model_x: LogisticRegression,
    model_d: LogisticRegression,
    feature_row: List[int],
) -> float:
    """
    Score aligné sur l’IA hybride : P(x_wins=1) * 1 + P(is_draw=1) * 0.5.
    Utilise les **deux** modèles (même formule que les feuilles du Minimax).
    """
    p_x1, _, p_d1, _ = predict_proba_for_row(model_x, model_d, feature_row)
    return p_x1 * 1.0 + p_d1 * 0.5


def best_move_for_x(
    model_x: LogisticRegression,
    model_d: LogisticRegression,
    board: List[str],
) -> Optional[int]:
    """
    IA **ML seul** (greedy, profondeur 1) : pour chaque coup possible de X,
    encoder le plateau résultant et calculer le score combiné des deux modèles ;
    choisir le coup qui **maximise** ce score.
    """
    candidates = [i for i in range(9) if board[i] == ""]
    if not candidates:
        return None
    best_i, best_score = None, float("-inf")
    for i in candidates:
        b = list(board)
        b[i] = "X"
        row = board_to_feature_row(b)
        s = _combined_ml_score(model_x, model_d, row)
        if s > best_score:
            best_score, best_i = s, i
    return best_i


def best_move_for_o(
    model_x: LogisticRegression,
    model_d: LogisticRegression,
    board: List[str],
) -> Optional[int]:
    """
    IA **ML seul** : pour chaque coup possible de O, même score combiné ;
    O cherche à **minimiser** ce score (moins favorable à X).
    """
    candidates = [i for i in range(9) if board[i] == ""]
    if not candidates:
        return None
    best_i, best_score = None, float("inf")
    for i in candidates:
        b = list(board)
        b[i] = "O"
        row = board_to_feature_row(b)
        s = _combined_ml_score(model_x, model_d, row)
        if s < best_score:
            best_score, best_i = s, i
    return best_i
