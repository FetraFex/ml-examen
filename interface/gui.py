import sys
import os
import flet as ft
import random
import time

# Ajout du chemin pour importer la logique depuis le dossier src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import get_best_move_ml # Assure-toi que cette fonction existe dans src/logic.py

def get_random_move(board):
    """IA de secours : choisit une case vide au hasard"""
    empty_cells = [i for i, cell in enumerate(board) if cell == ""]
    return random.choice(empty_cells) if empty_cells else None

def create_game_interface(page: ft.Page):
    # --- 1. CONFIGURATION DE LA PAGE ---
    page.title = "Morpion IA - Hackathon ISPM"
    page.window_width = 450
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- 2. ÉTAT DU JEU ---
    state = {
        "current_player": "X",
        "board": [""] * 9,
        "game_over": False
    }

    # --- 3. COMPOSANTS UI ---
    title = ft.Text("MORPION IA", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    status_text = ft.Text("Tour du joueur : X", size=18, color=ft.Colors.GREY_400)
    
    mode_selector = ft.Dropdown(
        label="Mode de jeu",
        value="vs Human",
        options=[
            ft.dropdown.Option("vs Human"),
            ft.dropdown.Option("vs IA (ML)"),
            ft.dropdown.Option("vs IA (Hybride)"),
        ],
        width=300,
    )

    # --- 4. FONCTIONS DE LOGIQUE INTERNE ---

    def check_winner():
        """Vérifie les conditions de victoire ou match nul (Étape 4)"""
        win_coords = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Lignes
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Colonnes
            [0, 4, 8], [2, 4, 6]             # Diagonales
        ]
        
        for coord in win_coords:
            if (state["board"][coord[0]] != "" and 
                state["board"][coord[0]] == state["board"][coord[1]] == state["board"][coord[2]]):
                
                state["game_over"] = True
                winner = state["board"][coord[0]]
                status_text.value = f"VICTOIRE POUR {winner} !"
                status_text.color = ft.Colors.GREEN_400
                return True

        if "" not in state["board"]:
            state["game_over"] = True
            status_text.value = "MATCH NUL !"
            status_text.color = ft.Colors.ORANGE_400
            return True
        
        return False

    def apply_move(index, player):
        """Applique le coup visuellement et logiquement"""
        state["board"][index] = player
        color = ft.Colors.BLUE if player == "X" else ft.Colors.RED
        
        # Mise à jour du bouton dans la liste buttons
        buttons[index].content = ft.Text(player, size=40, weight=ft.FontWeight.BOLD, color=color)
        buttons[index].disabled = True
        
        # Vérification immédiate de la fin de partie
        is_finished = check_winner()
        
        if not is_finished:
            # Change de joueur pour le prochain coup
            state["current_player"] = "O" if player == "X" else "X"
            status_text.value = f"Tour du joueur : {state['current_player']}"
            status_text.color = ft.Colors.GREY_400
        
        page.update()

    def cell_click(e):
        """Gère le clic humain et déclenche l'IA si besoin (Étape 4)"""
        if state["game_over"]:
            return
        
        index = e.control.data
        selected_mode = mode_selector.value 
        
        # Si la case est disponible
        if state["board"][index] == "":
            # --- TOUR DE L'HUMAIN ---
            apply_move(index, state["current_player"])
            
            # --- TOUR DE L'IA (si activé) ---
            if not state["game_over"] and selected_mode != "vs Human":
                status_text.value = f"L'IA ({selected_mode}) réfléchit..."
                status_text.color = ft.Colors.BLUE_200
                page.update()
                
                time.sleep(0.5) # Délai pour l'expérience utilisateur
                
                ai_move = None
                if selected_mode == "vs IA (ML)":
                    # Utilise le modèle .pkl via src/logic.py
                    ai_move = get_best_move_ml(state["board"])
                elif selected_mode == "vs IA (Hybride)":
                    # À terme, ici on mettra le Minimax + ML
                    ai_move = get_best_move_ml(state["board"])
                
                # Si l'IA trouve un coup, elle joue
                if ai_move is not None:
                    apply_move(ai_move, state["current_player"])

    # --- 5. CONSTRUCTION DE LA GRILLE ---
    buttons = []
    for i in range(9):
        btn = ft.Container(
            content=ft.Text("", size=40),
            alignment=ft.Alignment.CENTER, 
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_800,
            border_radius=10,
            on_click=cell_click,
            data=i 
        )
        buttons.append(btn)

    grid = ft.Column([
        ft.Row(buttons[0:3], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(buttons[3:6], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(buttons[6:9], alignment=ft.MainAxisAlignment.CENTER),
    ], spacing=10)

    # --- 6. ACTIONS GLOBALES ---
    def reset_game(e):
        page.clean()
        create_game_interface(page)

    reset_btn = ft.ElevatedButton(
        "Réinitialiser la partie", 
        on_click=reset_game,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_GREY_700
    )

    # --- 7. ASSEMBLAGE FINAL ---
    page.add(
        title,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        mode_selector,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        status_text,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        grid,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        reset_btn
    )