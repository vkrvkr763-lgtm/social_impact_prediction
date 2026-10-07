
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

POLICIES_PATH = BASE_DIR / "data" / "policies.csv"
DISCUSSIONS_PATH = BASE_DIR / "data" / "discussions.csv"
MODEL_PATH = BASE_DIR / "models" / "policy_stance_model.joblib"

# Initialize FastAPI
app = FastAPI(title="PolicyPulse API")

# Allow the local frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model once when the server starts
model = joblib.load(MODEL_PATH)


class DiscussionRequest(BaseModel):
    text: str = Field(min_length=3, max_length=5000)


@app.get("/")
def home():
    return {
        "message": "Welcome to PolicyPulse API",
        "model": "TF-IDF + Random Forest",
    }


@app.get("/policies")
def get_policies():
    df = pd.read_csv(POLICIES_PATH).fillna("")
    return df.to_dict(orient="records")


@app.post("/analyze")
def analyze_discussion(request: DiscussionRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Discussion text cannot be empty.",
        )

    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    return {
        "text": text,
        "stance": str(prediction),
        "confidence": float(max(probabilities)),
        "probabilities": {
            str(label): float(probability)
            for label, probability in zip(
                model.classes_, probabilities
            )
        },
        "model": "TF-IDF + Random Forest",
        "note": (
            "Experimental prediction from a small synthetic dataset; "
            "not a reliable measure of public opinion."
        ),
    }


@app.get("/analytics")
def get_analytics():
    df = pd.read_csv(DISCUSSIONS_PATH).fillna("")

    counts = df["stance_label"].value_counts().to_dict()
    total = len(df)

    return {
        "total_discussions": total,
        "synthetic_discussions": int(
            (df["is_real_discussion"] == False).sum()
        ),
        "stance_counts": {
            str(label): int(count)
            for label, count in counts.items()
        },
        "stance_percentages": {
            str(label): round(count / total * 100, 2)
            for label, count in counts.items()
        } if total else {},
        "note": "These are demo dataset statistics, not real public opinion.",
    }
