# Ordre recommandé (sujet hackathon)

1. **`generator.py` + `ressources/dataset2.csv`** (ou `dataset.csv`) — Génération Minimax / alpha-bêta (sans ça, pas de données propres pour l’entraînement « réel »).
2. **EDA dans le notebook** — Distributions, équilibre des classes, corrélation / heatmap (section dédiée dans `notebook.ipynb` ou notebook séparé).
3. **Baseline** — Déjà dans `baseline_logistic_regression.ipynb` (2 régressions logistiques + métriques).
4. **Modèles avancés** — Arbres, forêt, boosting, MLP dans le même notebook ou `src/ml_advanced.py`.
5. **Interface** — `streamlit_app.py` (test des modèles + modes de jeu) ; hybride Minimax + ML ensuite.
6. **README** — Résultats, coefficients, déséquilibre, comparaison, mode hybride.

**Interface de test ML (déjà ajoutée)** : lance `streamlit run streamlit_app.py` depuis `ml-examen/` pour valider les prédictions sur un plateau sans toucher au notebook.
