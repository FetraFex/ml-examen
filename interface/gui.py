import flet as ft

def create_game_interface(page: ft.Page):
    # Configuration de la fenêtre
    page.title = "Morpion IA - Hackathon ISPM"
    page.window_width = 450
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Titre principal
    title = ft.Text("MORPION IA", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    
    # Menu de sélection du mode (Étape 4 du sujet)
    mode_selector = ft.Dropdown(
        label="Mode de jeu",
        value="vs Human", # Mode par défaut
        options=[
            ft.dropdown.Option("vs Human"),
            ft.dropdown.Option("vs IA (ML)"),
            ft.dropdown.Option("vs IA (Hybride)"),
        ],
        width=300,
    )

    # Zone de message pour afficher le gagnant ou les probabilités
    status_text = ft.Text("À vous de jouer !", size=18, color=ft.Colors.GREY_700)

    # On ajoute les éléments à la page pour l'instant
    page.add(
        ft.Column(
            [
                title,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                mode_selector,
                status_text,
                # La grille sera ajoutée ici à l'étape suivante
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )