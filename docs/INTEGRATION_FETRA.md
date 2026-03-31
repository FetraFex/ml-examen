# Fusion manuelle : dossier `FETRA/ml-examen` → `ml-examen`

Les sources du clone **interface_project** (chemin local `examen/FETRA/ml-examen`) ont été **recopiées** dans le dépôt principal `examen/ml-examen`.

## Fichiers ajoutés ou mis à jour

- `src/dataset_generator.py`
- `src/generate_dataset_minimax.py` (ex-`main.py` FETRA ; ne pas confondre avec `api/main.py`)
- `src/generator_fetra.py` (ex-`generator.py`)
- `src/advanced_models/XGBoost.ipynb`, `MLPClassifier.ipynb`
- `ressources/dataset_morpion.csv`
- `ressources/dataset.csv` (écrasé par la version FETRA ; une copie sûre est aussi `dataset_fetra_branch.csv`)
- `ressources/model_xgboost_wins.pkl`, `model_xgboost_draw.pkl`, `model_mlp_wins.pkl`, `model_mlp_draw.pkl`

**Non modifié volontairement** : `ressources/dataset2.csv` (utilisé par `ml_baseline_service.py` et l’API).

## Commandes utiles

```bash
cd ml-examen
python -m src.generate_dataset_minimax   # régénère ressources/dataset.csv
```

Pour ouvrir les notebooks avancés : même kernel Jupyter que le reste du projet (`pip install xgboost`).
