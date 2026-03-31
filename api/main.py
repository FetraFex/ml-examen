"""
API REST pour le frontend React : prédictions baseline + coup IA.
Lancer depuis le dossier ml-examen :
  pip install fastapi uvicorn
  uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Racine du projet = parent de api/
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from src.board_encoding import board_to_feature_row
from src.ml_baseline_service import (
    best_move_for_o,
    best_move_for_x,
    load_dataset,
    predict_proba_for_row,
    train_baseline_models,
)

_models = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _models
    try:
        df = load_dataset()
        mx, md, meta = train_baseline_models(df)
        _models = (mx, md, meta)
    except FileNotFoundError as e:
        _models = None
        print(f"[api] Dataset manquant: {e}")
    yield


app = FastAPI(title="Morpion ML API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BoardIn(BaseModel):
    board: list[str] = Field(..., min_length=9, max_length=9)

    @field_validator("board")
    @classmethod
    def valid_cells(cls, v: list[str]) -> list[str]:
        for c in v:
            if c not in ("", "X", "O"):
                raise ValueError("Chaque case doit être '', 'X' ou 'O'.")
        return v


class PredictOut(BaseModel):
    p_x_wins_1: float
    p_x_wins_0: float
    p_is_draw_1: float
    p_is_draw_0: float


class AiMoveIn(BaseModel):
    board: list[str] = Field(..., min_length=9, max_length=9)
    role: str = Field(..., description="Joueur IA : X ou O")

    @field_validator("board")
    @classmethod
    def valid_cells(cls, v: list[str]) -> list[str]:
        for c in v:
            if c not in ("", "X", "O"):
                raise ValueError("Chaque case doit être '', 'X' ou 'O'.")
        return v

    @field_validator("role")
    @classmethod
    def valid_role(cls, v: str) -> str:
        if v not in ("X", "O"):
            raise ValueError("role doit être 'X' ou 'O'.")
        return v


class AiMoveOut(BaseModel):
    index: int | None


@app.get("/api/health")
def health():
    ok = _models is not None
    meta = _models[2] if _models else None
    return {"ok": ok, "dataset": meta}


@app.post("/api/predict", response_model=PredictOut)
def predict(body: BoardIn):
    if _models is None:
        raise HTTPException(503, "Dataset introuvable — placez ressources/dataset.csv")
    mx, md, _ = _models
    row = board_to_feature_row(body.board)
    p_x1, p_x0, p_d1, p_d0 = predict_proba_for_row(mx, md, row)
    return PredictOut(
        p_x_wins_1=p_x1,
        p_x_wins_0=p_x0,
        p_is_draw_1=p_d1,
        p_is_draw_0=p_d0,
    )


@app.post("/api/ai-move", response_model=AiMoveOut)
def ai_move(body: AiMoveIn):
    if _models is None:
        raise HTTPException(503, "Dataset introuvable")
    mx, md, _ = _models
    b = body.board
    if body.role == "X":
        idx = best_move_for_x(mx, md, b)
    else:
        idx = best_move_for_o(mx, b)
    return AiMoveOut(index=idx)
