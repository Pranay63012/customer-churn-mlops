import pandas as pd
from pathlib import Path


DATA_PATH = "data/raw/telco_customer_churn.csv"


def load_data(path: str) -> pd.DataFrame:
    if not Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)


if __name__ == "__main__":
    df = load_data(DATA_PATH)

    print("Dataset loaded")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())
