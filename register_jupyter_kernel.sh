#!/usr/bin/env bash
# Enregistre le Python du .venv comme noyau Jupyter nommé "Python (ml-examen .venv)".
# Ensuite dans JupyterLab : Kernel → Change Kernel… → choisir ce noyau.
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate
pip install -q ipykernel pandas scikit-learn
python -m ipykernel install --user --name=ml-examen --display-name="Python (ml-examen .venv)"
echo ""
echo "OK. Dans JupyterLab : Kernel → Change Kernel… → « Python (ml-examen .venv) »"
echo "Puis relance la première cellule (ou Run → Restart Kernel and Run All Cells)."
