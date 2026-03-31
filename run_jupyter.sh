#!/usr/bin/env bash
# Lance Jupyter avec la config du projet (timeouts websocket cohérents).
# Préférez "lab" pour que les clients qui appellent /lab/api/... (ex. certains IDE) soient alignés.
set -euo pipefail
cd "$(dirname "$0")"
export JUPYTER_CONFIG_DIR="$(pwd)/jupyter_config"
source .venv/bin/activate
exec jupyter lab "$@"
