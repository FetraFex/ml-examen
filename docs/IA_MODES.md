# Les deux modes d’IA (résumé)

## 1. IA **ML seul** (`best_move_for_x` / `best_move_for_o` dans `src/ml_baseline_service.py`)

| Aspect | Détail |
|--------|--------|
| **Idée** | Regarder **un seul coup à l’avance** (greedy). |
| **Modèles** | Les **deux** : score = `P(x_wins=1) × 1 + P(is_draw=1) × 0.5` sur le plateau **après** le coup testé. |
| **X** | Choisit le coup qui **maximise** ce score. |
| **O** | Choisit le coup qui **minimise** ce score. |
| **Différence avec l’hybride** | Pas d’arbre de jeu : pas de réponse à « et si l’adversaire joue le meilleur coup après ? » |

**API** : `POST /api/ai-move` (rôle `X` ou `O`).

---

## 2. IA **Hybride** (`src/hybrid_minimax.py`)

| Aspect | Détail |
|--------|--------|
| **Idée** | **Minimax** avec profondeur **3** + **élagage alpha-bêta**. |
| **Feuilles** | Même formule ML que ci-dessus (`_ml_score`). |
| **Modèles** | `model_xwins` et `model_draw` via `predict_proba` sur chaque position évaluée comme feuille. |
| **Différence** | Explore plusieurs coups d’affilée (jusqu’à 3 niveaux) et suppose que les deux joueurs jouent le mieux possible dans cet horizon. |

**API** : `POST /api/hybrid-move` (plateau seul ; le tour est déduit du nombre de X et O).

---

## Interface React

- **vs IA** → **ML seul** : heuristique greedy, rapide.  
- **vs IA** → **Hybride (Minimax 3 + ML)** : plus coûteux en calcul, mais cohérent avec un adversaire optimal sur 3 coups.
