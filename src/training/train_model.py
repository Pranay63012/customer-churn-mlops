import pandas as pd
import mlflow
import mlflow.sklearn
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score


PROCESSED_DATA_PATH = "data/processed/processed_data.csv"
MODEL_DIR = Path("models")


def train():
    df = pd.read_csv(PROCESSED_DATA_PATH)

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(
            n_estimators=200, random_state=42
        ),
    }

    mlflow.set_experiment("customer_churn_experiment")

    best_auc = 0.0
    best_model = None

    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            model.fit(X_train, y_train)

            preds = model.predict(X_test)
            probs = model.predict_proba(X_test)[:, 1]

            acc = accuracy_score(y_test, preds)
            auc = roc_auc_score(y_test, probs)

            mlflow.log_param("model_name", name)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("roc_auc", auc)

            mlflow.sklearn.log_model(model, name="model")

            if auc > best_auc:
                best_auc = auc
                best_model = model

    MODEL_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = MODEL_DIR / f"churn_model_{timestamp}"

    mlflow.sklearn.save_model(best_model, model_path)

    print("Training completed")
    print("Best ROC-AUC:", round(best_auc, 4))
    print("Model saved at:", model_path)


if __name__ == "__main__":
    train()
