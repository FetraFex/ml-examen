# Architecture du projet (cible hackathon)

```
ml-examen/
├── docs/
│   ├── ARCHITECTURE.md      # ce fichier
│   └── PROCHAINES_ETAPES.md
├── ressources/
│   └── dataset.csv          # généré par generator.py (à venir)
├── src/
│   ├── __init__.py
│   ├── board_encoding.py    # plateau → 18 features (même convention que le CSV)
│   └── ml_baseline_service.py  # entraînement + prédictions (aligné sur le notebook)
├── baseline_logistic_regression.ipynb  # baseline + EDA / modèles (ton travail)
├── streamlit_app.py         # interface : test ML + parties (sans modifier le notebook)
├── generator.py             # (à créer) dataset Minimax → ressources/dataset.csv
├── requirements.txt
├── run_jupyter.sh
└── README.md
```

**Séparation des rôles**

| Zone        | Rôle |
|------------|------|
| `generator.py` | Données (Minimax, CSV) |
| `src/` + notebook | Machine learning |
| `streamlit_app.py` | Expérience utilisateur (test + jeu) |
