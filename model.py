from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def train_model(df):
    X = df[["math score", "reading score", "writing score"]]
    y = df["average_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    return model, mae# model.py

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def train_model(df):
    # -----------------------------
    # 1. Feature Engineering
    # -----------------------------
    df = df.copy()

    # New Features
    df["score_gap"] = abs(df["math score"] - df["reading score"])

    df["test_prep_binary"] = df["test preparation course"].map({
        "completed": 1,
        "none": 0
    })

    # -----------------------------
    # 2. Features & Target
    # -----------------------------
    X = df.drop("writing score", axis=1)
    y = df["writing score"]

    # -----------------------------
    # 3. Column Types
    # -----------------------------
    categorical_cols = [
        "gender",
        "race/ethnicity",
        "parental level of education",
        "lunch",
        "test preparation course"
    ]

    numerical_cols = [
        "math score",
        "reading score",
        "score_gap",
        "test_prep_binary"
    ]

    # -----------------------------
    # 4. Preprocessing
    # -----------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numerical_cols)
        ]
    )

    # -----------------------------
    # 5. Model (Random Forest)
    # -----------------------------
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42
        ))
    ])

    # -----------------------------
    # 6. Train-Test Split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -----------------------------
    # 7. Train Model
    # -----------------------------
    model.fit(X_train, y_train)

    # -----------------------------
    # 8. Evaluate Model
    # -----------------------------
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    return model, mae, rmse, r2


# ----------------------------------------
# Prediction Function
# ----------------------------------------
def predict_scores(model, input_df):

    # Feature Engineering for input
    input_df = input_df.copy()

    input_df["score_gap"] = abs(
        input_df["math score"] - input_df["reading score"]
    )

    input_df["test_prep_binary"] = input_df[
        "test preparation course"
    ].map({
        "completed": 1,
        "none": 0
    })

    # Ensure column order
    expected_columns = [
        "gender",
        "race/ethnicity",
        "parental level of education",
        "lunch",
        "test preparation course",
        "math score",
        "reading score",
        "score_gap",
        "test_prep_binary"
    ]

    input_df = input_df[expected_columns]

    # Predict writing score
    predicted_writing = model.predict(input_df)[0]

    # Final score
    math_score = input_df["math score"].values[0]
    reading_score = input_df["reading score"].values[0]

    final_score = (math_score + reading_score + predicted_writing) / 3

    return predicted_writing, final_score