from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import os

app = FastAPI(
    title="Tunisia Real Estate MLOps API",
    description="API for predicting apartment prices in Tunisia using trained Machine Learning model",
    version="1.0.0"
)

# Robust Path Resolution for Model Artifact
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "real_estate_model.pkl")

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# Input Schema Validation
class PredictionInput(BaseModel):
    surface_m2: float = Field(..., gt=10, lt=2000, description="Surface area in m²")
    rooms: int = Field(..., gt=0, lt=20, description="Number of rooms")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")

    class Config:
        json_schema_extra = {
            "example": {
                "surface_m2": 120.0,
                "rooms": 3,
                "latitude": 36.8782,
                "longitude": 10.3247
            }
        }

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Tunisia Real Estate Price Prediction API",
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict_price(data: PredictionInput):
    if not model:
        raise HTTPException(status_code=500, detail="ML Model artifact not loaded.")
    
    try:
        features = [[data.surface_m2, data.rooms, data.latitude, data.longitude]]
        prediction = model.predict(features)[0]
        
        return {
            "surface_m2": data.surface_m2,
            "rooms": data.rooms,
            "latitude": data.latitude,
            "longitude": data.longitude,
            "predicted_price_tnd": round(float(prediction), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")