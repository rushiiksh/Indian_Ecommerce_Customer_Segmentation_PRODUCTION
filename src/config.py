from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'ecommerce_production.db'}")
    raw_data_dir: Path = PROJECT_ROOT / "data" / "raw"
    processed_data_dir: Path = PROJECT_ROOT / "data" / "processed"
    artifact_dir: Path = PROJECT_ROOT / "artifacts"
    report_dir: Path = PROJECT_ROOT / "reports"
    random_state: int = int(os.getenv("RANDOM_STATE", "42"))
    min_clusters: int = int(os.getenv("MIN_CLUSTERS", "2"))
    max_clusters: int = int(os.getenv("MAX_CLUSTERS", "8"))
    high_value_revenue_threshold: float = float(os.getenv("HIGH_VALUE_REVENUE_THRESHOLD", "40000"))
    churn_recency_threshold: int = int(os.getenv("CHURN_RECENCY_THRESHOLD", "180"))

settings = Settings()
for _path in (settings.artifact_dir, settings.report_dir, settings.processed_data_dir):
    _path.mkdir(parents=True, exist_ok=True)
