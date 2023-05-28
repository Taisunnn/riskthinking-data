import joblib

import pandas as pd
from fastapi import FastAPI

# Define dictionary to load model into
cache = {}


# FastAPI instance
app = FastAPI()


# On startup load model instead of loading model everytime on endpoint hit
@app.on_event("startup")
def startup():
    cache["stockmarket_model"] = joblib.load("model/model.pkl")


# Root page
@app.get("/")
def index():
    return {"Hello": "RiskThinkingAI!"}


# Predict endpoint
@app.get("/predict")
def predict(vol_moving_avg: float, adj_close_rolling_med: float):
    df = pd.DataFrame(
        {
            "vol_moving_avg": [vol_moving_avg],
            "adj_close_rolling_med": [adj_close_rolling_med],
        }
    )

    # Predict
    volume_prediction = cache["stockmarket_model"].predict(df)

    return volume_prediction[0]
