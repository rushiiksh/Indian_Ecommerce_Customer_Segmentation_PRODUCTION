import pandas as pd
from src.ml.preprocessing import prepare_features
from src.ml.segmentation import add_rfm_labels
from src.predict import CustomerPayload

def test_feature_preprocessing():
    df = pd.DataFrame({"recency":[1,2,3],"frequency":[3,4,5],"monetary":[100,200,300]})
    X, scaler = prepare_features(df)
    assert X.shape == (3,3)
    assert scaler is not None

def test_rfm_labels():
    df = pd.DataFrame({"recency":range(1,9),"frequency":range(8,0,-1),"monetary":[100,200,300,400,500,600,700,800]})
    out = add_rfm_labels(df)
    assert "rfm_segment" in out
    assert out["rfm_segment"].notna().all()

def test_payload_validation():
    p = CustomerPayload(customer_id="USR-1", recency=4, frequency=2, monetary_value=4500.5)
    assert p.frequency == 2
