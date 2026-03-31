import pandas as pd
import numpy as np
import os

# 1. Préparation des colonnes (18 features + 2 cibles)
columns = []
for i in range(9):
    columns.append(f'c{i}_x')
    columns.append(f'c{i}_o')

# 2. Génération de 100 lignes avec des états de cases valides
rows = []
for _ in range(100):
    row = []
    for _ in range(9):
        # Choix entre : Vide (0,0), X (1,0) ou O (0,1)
        etat = np.random.choice(['vide', 'X', 'O'])
        if etat == 'vide':
            row.extend([0, 0])
        elif etat == 'X':
            row.extend([1, 0])
        else:
            row.extend([0, 1])
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)

# 3. Ajout des cibles (Targets)
df['x_wins'] = np.random.randint(0, 2, size=100)
df['is_draw'] = np.random.randint(0, 2, size=100)

# 4. Sauvegarde
os.makedirs('../../ressources', exist_ok=True)
df.to_csv('../../ressources/test_dataset.csv', index=False)

print("Fichier ressources/test_dataset.csv généré.")