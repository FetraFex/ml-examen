#!/usr/bin/env bash
# Lance l'interface de test Streamlit (depuis le dossier ml-examen).
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate
exec streamlit run streamlit_app.py "$@"
