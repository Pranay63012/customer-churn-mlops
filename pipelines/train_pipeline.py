from src.preprocessing.preprocess import preprocess_data
from src.training.train_model import train


def run_pipeline():
    preprocess_data()
    train()


if __name__ == "__main__":
    run_pipeline()
