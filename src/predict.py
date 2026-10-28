import argparse
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from src.config import settings
from src.ml.business_rules import classify_customer

class CustomerPayload(BaseModel):
    customer_id: str = Field(min_length=1, max_length=100)
    recency: int = Field(ge=0)
    frequency: int = Field(gt=0)
    monetary_value: float = Field(ge=0)

def load_artifact():
    path = settings.artifact_dir / "segmentation.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}. Run `python -m src.train` first.")
    return joblib.load(path)

def infer_customer_segment(input_data: dict) -> dict:
    payload = CustomerPayload.model_validate(input_data)
    artifact = load_artifact()
    frame = pd.DataFrame([{
        "recency": payload.recency,
        "frequency": payload.frequency,
        "monetary": payload.monetary_value,
    }])[artifact["features"]]
    cluster = int(artifact["model"].predict(artifact["scaler"].transform(frame))[0])
    return {
        "customer_id": payload.customer_id,
        "assigned_cluster": cluster,
        "strategic_persona": classify_customer(payload.recency, payload.frequency, payload.monetary_value),
        "model_version": artifact["model_version"],
    }

def main():
    p = argparse.ArgumentParser(description="Infer an e-commerce customer segment")
    p.add_argument("--customer-id", required=True)
    p.add_argument("--recency", type=int, required=True)
    p.add_argument("--frequency", type=int, required=True)
    p.add_argument("--monetary-value", type=float, required=True)
    args = p.parse_args()
    print(infer_customer_segment(vars(args)))

if __name__ == "__main__": main()
