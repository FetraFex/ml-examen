from dataset_generator import (
    X,
    O,
    VIDE,
    verifier_victoire,
    minimax_pure,
    encode_etat,
    generer_tous_les_succ,
    minimax,
)
import pandas as pd


etats_uniques = set()
generer_tous_les_succ([VIDE] * 9, X, etats_uniques)

print(f"{len(etats_uniques)} états trouvés pour X. Calcul des labels...")
dataset = []

for state in etats_uniques:
    # Minimax pour obtenir le résultat en jeu parfait
    result = minimax(list(state), True, -float("inf"), float("inf"))

    # Encodage et cibles
    row = encode_etat(state)
    row["x_wins"] = 1 if result == 1 else 0
    row["is_draw"] = 1 if result == 0 else 0
    dataset.append(row)

# Export CSV
df = pd.DataFrame(dataset)
df.to_csv("ressources/dataset.csv", index=False)
print("✅ Fichier ressources/dataset.csv généré avec succès !")
