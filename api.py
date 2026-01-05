from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Housing Price Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, restrict to frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load artifacts
class ModelArtifacts:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_columns = None

    def load(self):
        try:
            with open('models/house_price_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('models/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            with open('models/model_columns.pkl', 'rb') as f:
                self.model_columns = pickle.load(f)
            print("Artifacts loaded successfully")
        except FileNotFoundError:
            print("Artifacts not found. Please run 'python main.py' first.")

artifacts = ModelArtifacts()
artifacts.load()

class HouseFeatures(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str
    guestroom: str
    basement: str
    hotwaterheating: str
    airconditioning: str
    parking: int
    prefarea: str
    furnishingstatus: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Housing Price Prediction API"}

@app.post("/predict")
def predict_price(features: HouseFeatures):
    if artifacts.model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Convert input to DataFrame
    input_data = pd.DataFrame([features.dict()])
    
    # Preprocess
    # 1. Encode categorical variables
    input_encoded = pd.get_dummies(input_data, drop_first=True)
    
    # 2. Align columns with training data
    # Get missing columns in the training test
    missing_cols = set(artifacts.model_columns) - set(input_encoded.columns)
    # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        input_encoded[c] = 0
        
    # Ensure the order of column in the test set is in the same order than in train set
    input_encoded = input_encoded[artifacts.model_columns]
    
    # 3. Scale features
    input_scaled = artifacts.scaler.transform(input_encoded)
    
    # 4. Predict
    prediction = artifacts.model.predict(input_scaled)
    
    return {
        "predicted_price": float(prediction[0]),
        "currency": "USD"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
