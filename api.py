# api.py

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from model import train_model, predict_scores
from decision import analyze_performance
from ai_module import generate_ai_analysis
from database import insert_prediction, create_table
from util import load_data

app = FastAPI()

# ---------- LOAD EVERYTHING ----------
df = load_data()
model, mae, rmse, r2 = train_model(df)

create_table()

# ---------- INPUT SCHEMA ----------
class StudentInput(BaseModel):
    gender: str
    race: str
    parental: str
    lunch: str
    prep: str
    math: float
    reading: float


# ---------- PREDICT ENDPOINT ----------
@app.post("/predict")
def predict(data: StudentInput):

    # Convert input to DataFrame
    input_df = pd.DataFrame({
        "gender": [data.gender],
        "race/ethnicity": [data.race],
        "parental level of education": [data.parental],
        "lunch": [data.lunch],
        "test preparation course": [data.prep],
        "math score": [data.math],
        "reading score": [data.reading]
    })

    # ---------- MODEL ----------
    predicted_writing, final_score = predict_scores(model, input_df)

    # ---------- WEAK SUBJECT ----------
    scores = {
        "Math": data.math,
        "Reading": data.reading,
        "Writing": predicted_writing
    }
    weak_subject = min(scores, key=scores.get)

    # ---------- DECISION ----------
    level, risk, recommendation = analyze_performance(final_score, weak_subject)

    # ---------- AI ----------
    ai_data = {
        "gender": data.gender,
        "race": data.race,
        "parental": data.parental,
        "lunch": data.lunch,
        "prep": data.prep,
        "math": data.math,
        "reading": data.reading,
        "writing": round(predicted_writing, 2),
        "final_score": round(final_score, 2),
        "level": level,
        "risk": risk,
        "weak_subject": weak_subject
    }

    ai_output = generate_ai_analysis(ai_data)

    # ---------- STORE ----------
    db_data = {
        "gender": data.gender,
        "race": data.race,
        "parental": data.parental,
        "lunch": data.lunch,
        "prep": data.prep,
        "math": data.math,
        "reading": data.reading,
        "writing": predicted_writing,
        "final_score": final_score,
        "level": level,
        "risk": risk,
        "weak_subject": weak_subject
    }

    insert_prediction(db_data)

    # ---------- RESPONSE ----------
    return {
        "predicted_writing": round(predicted_writing, 2),
        "final_score": round(final_score, 2),
        "performance_level": level,
        "risk_level": risk,
        "weak_subject": weak_subject,
        "recommendation": recommendation,
        "ai_analysis": ai_output
    }


# ---------- HISTORY ENDPOINT ----------
@app.get("/history")
def get_history():
    from database import fetch_all
    return fetch_all()