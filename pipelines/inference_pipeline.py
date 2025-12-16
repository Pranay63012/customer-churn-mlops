import joblib
import pandas as pd
import mlflow.sklearn
from pathlib import Path


PREPROCESSOR_PATH = "models/preprocessor.pkl"
MODEL_DIR = Path("models")


def load_latest_model():
    model_dirs = sorted(
        [d for d in MODEL_DIR.iterdir() if d.is_dir() and d.name.startswith("churn_model_")],
        reverse=True
    )

    if not model_dirs:
        raise FileNotFoundError("No trained churn model found")

    return mlflow.sklearn.load_model(str(model_dirs[0]))


def predict(input_df: pd.DataFrame):
    model = load_latest_model()
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    X = preprocessor.transform(input_df)

    prob = model.predict_proba(X)[:, 1][0]
    pred = int(prob >= 0.5)

    return pred, prob
