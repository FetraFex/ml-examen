from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

# ============================================================================================
# ================= Étape 2 : Baseline : Régression Logistique  (×2) =========================
# ============================================================================================

def load_dataset() -> tuple[pd.DataFrame, Path]:
    # Structure de dossier
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "ressources" / "dataset_morpion.csv"

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {dataset_path}\n"
            "Vérifie que le fichier ressources/dataset_morpion.csv existe."
        )

    return pd.read_csv(dataset_path), dataset_path

def plot_coefficients(model, title):
    """Visualise les 18 coefficients mappés sur le plateau 3x3"""
    # Les 18 coefs : 9 pour X, 9 pour O
    coefs = model.coef_[0]
    
    # Découpage des coefficients pour X (indices pairs) et O (indices impairs)
    coefs_x = coefs[0::2].reshape(3, 3)
    coefs_o = coefs[1::2].reshape(3, 3)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(title, fontsize=14)
    
    # Carte pour ci_x (Pions X)
    sns.heatmap(coefs_x, annot=True, cmap='RdBu_r', center=0, ax=ax1)
    ax1.set_title('Influence Pions X (ci_x)')
    
    # Carte pour ci_o (Pions O)
    sns.heatmap(coefs_o, annot=True, cmap='RdBu_r', center=0, ax=ax2)
    ax2.set_title('Influence Pions O (ci_o)')
    
    plt.tight_layout()
    plt.show()

def main() -> None:
    df, dataset_path = load_dataset()

    feature_columns = [col for col in df.columns if col.startswith("c")]
    X = df[feature_columns]

    y_x_wins = df["x_wins"]
    y_is_draw = df["is_draw"]

    # Split pour le modèle x_wins
    X_train, X_test, y_x_train, y_x_test = train_test_split(
        X, y_x_wins, test_size=0.2, random_state=42
    )

    # Split pour le modèle is_draw (même random_state)
    _, _, y_draw_train, y_draw_test = train_test_split(
        X, y_is_draw, test_size=0.2, random_state=42
    )

    # Initialisation et entraînement
    model_x_wins = LogisticRegression(max_iter=1000)
    model_is_draw = LogisticRegression(max_iter=1000)

    model_x_wins.fit(X_train, y_x_train)
    model_is_draw.fit(X_train, y_draw_train)

    # Prédictions
    pred_x_wins = model_x_wins.predict(X_test)
    pred_is_draw = model_is_draw.predict(X_test)

    # Affichage des métriques
    print("=== Entraînement Régression Logistique ===")
    print(f"Dataset chargé : {dataset_path}")
    print(f"Nombre total de lignes : {len(df)}")
    print(f"Nombre de features : {X.shape[1]}\n")

    print("--- Modèle 1 : x_wins ---")
    print("Accuracy :", accuracy_score(y_x_test, pred_x_wins))
    print("F1-Score :", f1_score(y_x_test, pred_x_wins, zero_division=0))
    print("Matrice de confusion :")
    print(confusion_matrix(y_x_test, pred_x_wins))
    
    # Visualisation des coefficients (Obligatoire E2)
    plot_coefficients(model_x_wins, "Coefficients - Prediction Victoire de X")

    print("\n--- Modèle 2 : is_draw ---")
    print("Accuracy :", accuracy_score(y_draw_test, pred_is_draw))
    print("F1-Score :", f1_score(y_draw_test, pred_is_draw, zero_division=0))
    print("Matrice de confusion :")
    print(confusion_matrix(y_draw_test, pred_is_draw))
    
    # Visualisation des coefficients (Obligatoire E2)
    plot_coefficients(model_is_draw, "Coefficients - Prediction Match Nul")


# ============================================================================================
# ============== FIN _ Étape 2 : Baseline : Régression Logistique  (×2) ======================
# ============================================================================================


if __name__ == "__main__":
    main()