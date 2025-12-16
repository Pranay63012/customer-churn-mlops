from fastapi import FastAPI, HTTPException
import pandas as pd

from api.schemas import ChurnInput
from pipelines.inference_pipeline import predict

app = FastAPI()


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/predict")
def predict_churn(data: ChurnInput):
    try:
        df = pd.DataFrame([data.dict()])

        pred, prob = predict(df)

        return {
            "churn_prediction": pred,
            "churn_probability": round(prob, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
