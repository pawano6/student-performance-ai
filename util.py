import pandas as pd

def load_data():
    df = pd.read_csv("data/StudentsPerformance.csv")

    df["average_score"] = (
        df["math score"] + df["reading score"] + df["writing score"]
    ) / 3

    return df