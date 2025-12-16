import pandas as pd
import mlflow.sklearn
from sklearn.metrics import accuracy_score, roc_auc_score


MODEL_PATH = "models/churn_model"
DATA_PATH = "data/processed/processed_data.csv"


def evaluate():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    model = mlflow.sklearn.load_model(MODEL_PATH)

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    acc = accuracy_score(y, preds)
    auc = roc_auc_score(y, probs)

    print("Accuracy:", round(acc, 3))
    print("ROC-AUC:", round(auc, 3))


if __name__ == "__main__":
    evaluate()
