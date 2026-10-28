import json
import logging
from datetime import datetime, timezone
import joblib
from src.config import settings
from src.features import build_customer_features, save_features
from src.ml.preprocessing import prepare_features, FEATURE_COLUMNS
from src.ml.clustering import select_best_k, train_cluster_model
from src.ml.segmentation import add_rfm_labels

log = logging.getLogger(__name__)

def train():
    df = build_customer_features()
    save_features(df)
    X, scaler = prepare_features(df)
    k, metrics = select_best_k(X, settings.min_clusters, settings.max_clusters, settings.random_state)
    model = train_cluster_model(X, k, settings.random_state)
    df["cluster"] = model.predict(X)
    metrics.to_csv(settings.report_dir / "cluster_model_metrics.csv", index=False)
    add_rfm_labels(df).to_csv(settings.report_dir / "customer_segments.csv", index=False)
    df.groupby("cluster").agg(customers=("customer_id","count"), avg_recency=("recency","mean"), avg_frequency=("frequency","mean"), avg_monetary=("monetary","mean"), total_revenue=("monetary","sum"), total_profit=("profit","sum")).reset_index().to_csv(settings.report_dir / "cluster_summary.csv", index=False)
    artifact = {"model": model, "scaler": scaler, "features": FEATURE_COLUMNS, "best_k": k, "model_version": "1.0.0", "trained_at": datetime.now(timezone.utc).isoformat()}
    joblib.dump(artifact, settings.artifact_dir / "segmentation.joblib")
    (settings.artifact_dir / "metadata.json").write_text(json.dumps({k:v for k,v in artifact.items() if k not in {"model","scaler"}}, indent=2))
    log.info("Training complete: K=%d, rows=%d", k, len(df))
    return artifact

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    train()
