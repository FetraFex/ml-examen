X = 1
O = -1
VIDE = 0


def verifier_victoire(grille):
    vict_position = [
        (0, 1, 2),  # Lignes
        (3, 4, 5),  # Lignes
        (6, 7, 8),  # Lignes
        (0, 3, 6),  # Colonnes
        (1, 4, 7),  # Colonnes
        (2, 5, 8),  # Colonnes
        (0, 4, 8),  # Diagonales
        (2, 4, 6),  # Diagonales
    ]

    for pos in vict_position:
        if grille[pos[0]] == grille[pos[1]] == grille[pos[2]] != VIDE:
            return grille[pos[0]]  # Retourne 1 (si X gagne) et -1 (si O gagne)
        if VIDE not in grille:  # s'il n'y a plus de case vide
            return 0  # Match nul
        return None  # Partie en cours


memo = {}


def minimax(grille, is_maximizing, alpha, beta):
    """Algorithme Minimax avec élagage Alpha-Bêta."""
    state = tuple(grille)
    if state in memo:
        return memo[state]

    res = verifier_victoire(grille)
    if res is not None:
        return res

    if is_maximizing:  # Tour de X
        best_score = -float("inf")
        for i in range(9):
            if grille[i] == VIDE:
                grille[i] = X
                score = minimax(grille, False, alpha, beta)
                grille[i] = VIDE
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        memo[state] = best_score
        return best_score
    else:  # Tour de O
        best_score = float("inf")
        for i in range(9):
            if grille[i] == VIDE:
                grille[i] = O
                score = minimax(grille, True, alpha, beta)
                grille[i] = VIDE
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        memo[state] = best_score
        return best_score


def minimax_pure(grille, is_maximizing):
    """
    Version standard du Minimax (sans élagage Alpha-Bêta).
    Avec élagage Alpha Bêta le ao anaty sujet fa tsy haiko ity raha ilaina ihany
    """
    # Verifier si l'état (Noeud) est déjà dans
    etat = tuple(grille)
    if etat in memo:
        return memo[etat]

    # Vérifier s'il y a un gagnant
    res = verifier_victoire(grille)
    if res is not None:
        return res

    if is_maximizing:  # Tour de X (cherche à maximiser le score)
        best_score = -float("inf")
        for i in range(9):
            if grille[i] == VIDE:
                grille[i] = X
                # Appel récursif simple
                score = minimax_pure(grille, False)
                grille[i] = VIDE
                best_score = max(score, best_score)

        memo[etat] = best_score
        return best_score

    else:  # Tour de O (cherche à minimiser le score)
        best_score = float("inf")
        for i in range(9):
            if grille[i] == VIDE:
                grille[i] = O
                # Appel récursif simple
                score = minimax_pure(grille, True)
                grille[i] = VIDE
                best_score = min(score, best_score)

        memo[etat] = best_score
        return best_score


def encode_etat(grille):
    """Une fonction pour structurer le dataset comme dans l'énoncé"""
    encoded = {}
    for i in range(9):
        encoded[f"c{i}_x"] = 1 if grille[i] == X else 0
        encoded[f"c{i}_o"] = 1 if grille[i] == O else 0
    return encoded


def generer_tous_les_succ(grille, current_player, all_etats):
    """Parcour l'arbre pour collecter tous les états uniques"""
    etat = tuple(grille)
    if etat in all_etats:
        return

    # On n'enregistre que si c'est au tour de X
    # (X a joué autant de fois que O)
    if grille.count(X) == grille.count(O):
        all_etats.add(etat)

    res = verifier_victoire(grille)
    if res is not None:
        return

    for i in range(9):
        if grille[i] == VIDE:
            grille[i] = current_player
            generer_tous_les_succ(grille, -current_player, all_etats)
            grille[i] = VIDE
