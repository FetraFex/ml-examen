"""
Interface Streamlit : test des modèles baseline + parties Humain/Humain et Humain/IA.
N'altère pas baseline_logistic_regression.ipynb — utilise src/ml_baseline_service.py.

Lancer depuis ml-examen :
  source .venv/bin/activate
  streamlit run streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src.board_encoding import board_to_feature_row, empty_board
from src.ml_baseline_service import (
    best_move_for_o,
    best_move_for_x,
    load_dataset,
    predict_proba_for_row,
    train_baseline_models,
)

WINS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def check_winner(board: list[str]) -> str | None:
    for a, b, c in WINS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def board_full(board: list[str]) -> bool:
    return all(board[i] for i in range(9))


@st.cache_resource
def cached_models():
    df = load_dataset()
    return train_baseline_models(df)


def main() -> None:
    st.set_page_config(page_title="Morpion — test ML", layout="wide")
    st.title("Morpion — test baseline + parties")

    try:
        model_x, model_d, meta = cached_models()
    except FileNotFoundError as e:
        st.error(str(e))
        st.info("Place `ressources/dataset.csv` puis relance l'application.")
        return

    st.sidebar.success(f"Modèles OK — {meta['n_samples']} lignes dans le CSV.")

    mode = st.sidebar.radio(
        "Mode",
        [
            "Test ML (prédictions sur un plateau)",
            "Humain vs Humain",
            "Humain vs IA (ML)",
            "IA hybride (Minimax + ML) — à venir",
        ],
        index=0,
    )

    if mode == "IA hybride (Minimax + ML) — à venir":
        st.info(
            "Prévu par le sujet : Minimax (prof. 3) + ML comme fonction d'évaluation. "
            "À ajouter dans un module dédié, sans modifier le notebook baseline."
        )
        return

    # ----- Test ML -----
    if mode == "Test ML (prédictions sur un plateau)":
        st.subheader("Encoder le plateau (9 cases) puis lire P(x_wins) et P(is_draw)")
        if "test_board" not in st.session_state:
            st.session_state.test_board = empty_board()

        tb = st.session_state.test_board
        opts = ["vide", "X", "O"]
        st.caption("Choisis l’état de chaque case :")
        cols = st.columns(3)
        for i in range(9):
            with cols[i % 3]:
                cur = tb[i] if tb[i] else "vide"
                if cur not in opts:
                    cur = "vide"
                label = f"Case {i}"
                choice = st.selectbox(
                    label,
                    opts,
                    index=opts.index(cur) if cur in opts else 0,
                    key=f"sb_{i}",
                )
                tb[i] = "" if choice == "vide" else choice

        st.session_state.test_board = tb
        row = board_to_feature_row(tb)
        p_x1, p_x0, p_d1, p_d0 = predict_proba_for_row(model_x, model_d, row)

        c1, c2 = st.columns(2)
        with c1:
            st.metric("P(x_wins = 1)", f"{p_x1:.4f}")
            st.caption(f"P(x_wins = 0) = {p_x0:.4f}")
        with c2:
            st.metric("P(is_draw = 1)", f"{p_d1:.4f}")
            st.caption(f"P(is_draw = 0) = {p_d0:.4f}")

        if st.button("Réinitialiser le plateau"):
            st.session_state.test_board = empty_board()
            st.rerun()
        return

    # ----- Humain vs Humain -----
    if mode == "Humain vs Humain":
        st.subheader("Humain vs Humain")
        if "hvh_board" not in st.session_state:
            st.session_state.hvh_board = empty_board()
            st.session_state.hvh_turn = "X"

        b = st.session_state.hvh_board
        turn = st.session_state.hvh_turn
        w = check_winner(b)
        full = board_full(b)

        st.write(f"Tour : **{turn}**")
        if w:
            st.success(f"Gagnant : {w}")
        elif full:
            st.info("Match nul.")

        done = w or full
        for r in range(3):
            row_cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                with row_cols[c]:
                    lab = b[idx] if b[idx] else " "
                    if st.button(
                        lab,
                        key=f"hvh_{idx}",
                        disabled=done or bool(b[idx]),
                    ):
                        b[idx] = turn
                        st.session_state.hvh_turn = "O" if turn == "X" else "X"
                        st.session_state.hvh_board = b
                        st.rerun()

        if st.button("Nouvelle partie (HvH)"):
            st.session_state.hvh_board = empty_board()
            st.session_state.hvh_turn = "X"
            st.rerun()
        return

    # ----- Humain vs IA -----
    if mode == "Humain vs IA (ML)":
        st.subheader("Humain vs IA (heuristique : max P(x_wins) pour X, min pour O)")
        human = st.radio("Tu joues", ["X (tu commences)", "O (l’IA commence)"], horizontal=True)
        human_is_x = human.startswith("X")
        key_b, key_init = "hvm_board", "hvm_init"

        if key_b not in st.session_state:
            st.session_state[key_b] = empty_board()
            st.session_state[key_init] = False

        b = list(st.session_state[key_b])
        w = check_winner(b)
        full = board_full(b)

        # IA joue X en premier si tu es O
        if not human_is_x and not any(b) and not w and not st.session_state[key_init]:
            mv = best_move_for_x(model_x, model_d, b)
            if mv is not None:
                b[mv] = "X"
                st.session_state[key_b] = b
                st.session_state[key_init] = True
                st.rerun()

        if w:
            st.success(f"Gagnant : {w}")
        elif full:
            st.info("Match nul.")

        nx = sum(1 for x in b if x == "X")
        no = sum(1 for x in b if x == "O")
        if human_is_x:
            human_turn = nx == no and not w and not full
        else:
            human_turn = nx > no and not w and not full

        for r in range(3):
            row_cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                with row_cols[c]:
                    lab = b[idx] if b[idx] else " "
                    dis = bool(b[idx]) or w or full or not human_turn
                    if st.button(lab, key=f"hvm_{idx}", disabled=dis):
                        if human_turn and human_is_x:
                            b[idx] = "X"
                        elif human_turn and not human_is_x:
                            b[idx] = "O"
                        st.session_state[key_b] = b
                        # coup IA
                        b2 = list(st.session_state[key_b])
                        w2 = check_winner(b2)
                        f2 = board_full(b2)
                        if not w2 and not f2:
                            if human_is_x:
                                mv = best_move_for_o(model_x, b2)
                                if mv is not None:
                                    b2[mv] = "O"
                            else:
                                mv = best_move_for_x(model_x, model_d, b2)
                                if mv is not None:
                                    b2[mv] = "X"
                            st.session_state[key_b] = b2
                        st.rerun()

        if st.button("Nouvelle partie (H vs IA)"):
            st.session_state[key_b] = empty_board()
            st.session_state[key_init] = False
            st.rerun()


if __name__ == "__main__":
    main()
