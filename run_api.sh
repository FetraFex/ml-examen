#!/usr/bin/env bash
# API FastAPI pour le frontend React (port 8000).
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate
exec uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
