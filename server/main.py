from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Morpion AI API")

# --- CONFIGURATION CORS ---
# Très important pour que React puisse communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, remplacez par l'URL de votre site React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CHARGEMENT DU MODÈLE ---
# Assurez-vous que le fichier .pkl est dans le dossier /models
try:
    model = joblib.load("models/model_xgboost_wins.pkl")
    print("✅ Modèle chargé avec succès")
except Exception as e:
    print(f"❌ Erreur de chargement du modèle : {e}")


# --- SCHÉMA DES DONNÉES ---
class GameState(BaseModel):
    features: list  # La liste des 18 features (ex: [1,0,0,1...])


# --- ENDPOINTS ---
@app.get("/")
def home():
    return {"message": "API Morpion IA en ligne"}


@app.post("/predict")
async def get_prediction(data: GameState):
    # Conversion en format numpy pour le modèle
    input_array = np.array(data.features).reshape(1, -1)

    # Prédiction des probabilités
    # [probabilité_perte, probabilité_victoire]
    prediction = model.predict_proba(input_array)
    win_probability = prediction[0][1]

    return {"win_probability": round(float(win_probability), 4), "status": "success"}
