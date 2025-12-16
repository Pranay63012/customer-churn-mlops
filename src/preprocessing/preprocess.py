import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
from pathlib import Path
import numpy as np


RAW_DATA_PATH = "data/raw/telco_customer_churn.csv"
PROCESSED_DATA_PATH = "data/processed/processed_data.csv"
PREPROCESSOR_PATH = "models/preprocessor.pkl"


def preprocess_data():
    df = pd.read_csv(RAW_DATA_PATH)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)

    y = df["Churn"].map({"Yes": 1, "No": 0})
    X = df.drop(columns=["Churn", "customerID"])

    categorical_cols = X.select_dtypes(include="object").columns
    numerical_cols = X.select_dtypes(exclude="object").columns

    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ]
    )

    X_processed = preprocessor.fit_transform(X)

    if not isinstance(X_processed, np.ndarray):
        X_processed = X_processed.toarray()

    Path("models").mkdir(exist_ok=True)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    processed_df = pd.DataFrame(X_processed)
    processed_df["Churn"] = y.values

    processed_df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Preprocessing completed")


if __name__ == "__main__":
    preprocess_data()
