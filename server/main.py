from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Initialisation de l'application
app = FastAPI(title="Morpion Logistic Regression API")

# Configuration CORS pour React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production (ex: ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle de régression logistique
MODEL_PATH = "models/tic_tac_toe_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print(f"Modèle chargé avec succès : {MODEL_PATH}")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None


# Schéma de données attendu en entrée (les 18 colonnes binaires)
class GameState(BaseModel):
    features: list


@app.get("/")
def health_check():
    return {"status": "online", "model": "LogisticRegression"}


@app.post("/predict")
async def predict(data: GameState):
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé sur le serveur")

    if len(data.features) != 18:
        raise HTTPException(
            status_code=400, detail="Le modèle attend exactement 18 caractéristiques"
        )

    try:
        # Transformation de la liste en tableau NumPy (1, 18)
        input_data = np.array(data.features).reshape(1, -1)

        # Calcul de la probabilité de victoire (classe 1)
        # predict_proba renvoie [[prob_0, prob_1]]
        probabilities = model.predict_proba(input_data)
        win_probability = float(probabilities[0][1])

        # Prédiction finale (0 ou 1)
        prediction = int(model.predict(input_data)[0])

        return {
            "win_probability": round(win_probability, 4),
            "prediction": prediction,
            "message": (
                "Victoire probable de X"
                if prediction == 1
                else "Pas de victoire détectée"
            ),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="https://ml-examen.vercel.app/", port=8000)
