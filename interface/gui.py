import sys
import os
import flet as ft
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import get_ml_features, get_best_move_ml

def get_random_move(board):
    # Liste des index des cases vides
    empty_cells = [i for i, cell in enumerate(board) if cell == ""]
    if empty_cells:
        return random.choice(empty_cells)
    return None

def create_game_interface(page: ft.Page):
    # CONFIGURATION DE LA PAGE
    page.title = "Morpion IA - Hackathon ISPM"
    page.window_width = 450
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # VARIABLES D'ÉTAT
    state = {
        "current_player": "X",
        "board": [""] * 9,
        "game_over": False
    }

    # COMPOSANTS DE TEXTE
    title = ft.Text("MORPION IA", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    status_text = ft.Text("Tour du joueur : X", size=18, color=ft.Colors.GREY_400)

    # Logique d'encodage pour le ML
    def get_features():
        features = []
        for cell in state["board"]:
            if cell == "X":
                features.extend([1, 0]) # ci_x = 1, ci_o = 0
            elif cell == "O":
                features.extend([0, 1]) # ci_x = 0, ci_o = 1
            else:
                features.extend([0, 0]) # ci_x = 0, ci_o = 0
        return features

    # LOGIQUE DU CLIC
    def cell_click(e):
        # 1. EMPÊCHER DE JOUER SI LA PARTIE EST FINIE
        if state["game_over"]:
            return
        
        index = e.control.data # L'index 0-8 de la case cliquée
        selected_mode = mode_selector.value 
        
        # 2. TOUR DE L'HUMAIN (X)
        if state["board"][index] == "":
            apply_move(index, state["current_player"])
            
            # 3. TOUR DE L'IA (Si on n.est pas en mode "vs Human" et que le jeu continue)
            if not state["game_over"] and selected_mode != "vs Human":
                
                # Petit retour visuel pour l'utilisateur
                status_text.value = f"L'IA ({selected_mode}) réfléchit..."
                status_text.color = ft.Colors.BLUE_200
                page.update()
                
                # Simulation d'un temps de réflexion (0.5 seconde)
                import time
                time.sleep(0.5)
                
                # Appel de l'IA (On utilise le hasard pour l'instant)
                ai_move = get_random_move(state["board"])
                
                if ai_move is not None:
                    apply_move(ai_move, "O")

    def apply_move(index, player):
        state["board"][index] = player
        color = ft.Colors.BLUE if player == "X" else ft.Colors.RED
        
        # Mise à jour visuelle du bouton spécifique dans la liste
        buttons[index].content = ft.Text(player, size=40, weight=ft.FontWeight.BOLD, color=color)
        buttons[index].disabled = True
        
        # Vérification de victoire/nul (À coder à l'étape suivante)
        check_winner()
        
        if not state["game_over"]:
            state["current_player"] = "O" if player == "X" else "X"
            status_text.value = f"Tour du joueur : {state['current_player']}"
        
        page.update()

    def get_best_move_simulation():
        # Simulation : l'IA prend la première case vide
        for i, cell in enumerate(state["board"]):
            if cell == "": return i
        return None
    
    def check_winner():
        # Les 8 combinaisons gagnantes au Morpion
        win_coords = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontales
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Verticales
            [0, 4, 8], [2, 4, 6]             # Diagonales
        ]
        
        for coord in win_coords:
            if (state["board"][coord[0]] != "" and 
                state["board"][coord[0]] == state["board"][coord[1]] == state["board"][coord[2]]):
                
                state["game_over"] = True
                winner = state["board"][coord[0]]
                status_text.value = f"JOUEUR {winner} A GAGNÉ !"
                status_text.color = ft.Colors.GREEN_400
                return

        # Vérifier le match nul
        if "" not in state["board"]:
            state["game_over"] = True
            status_text.value = "MATCH NUL !"
            status_text.color = ft.Colors.ORANGE_400

    # CRÉATION DES 9 BOUTONS
    buttons = []
    for i in range(9):
        btn = ft.Container(
            content=ft.Text("", size=40),
            # Correction de l'alignement ici :
            alignment=ft.Alignment.CENTER, 
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_800,
            border_radius=10,
            on_click=cell_click,
            data=i 
        )
        buttons.append(btn)

    # MISE EN PAGE DE LA GRILLE
    grid = ft.Column([
        ft.Row(buttons[0:3], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(buttons[3:6], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(buttons[6:9], alignment=ft.MainAxisAlignment.CENTER),
    ], spacing=10)

    # SÉLECTEUR DE MODE
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

    # BOUTON RESET
    def reset_game(e):
        page.clean()
        create_game_interface(page)

    reset_btn = ft.ElevatedButton(
        "Réinitialiser", 
        on_click=reset_game,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_GREY_700
    )

    # AJOUT FINAL À LA PAGE
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