from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.config import settings
from src.db import engine

RFM_QUERY = """
WITH customer_summary AS (
 SELECT o.customer_id, o.customer_name, MAX(o.order_date) AS last_order,
        COUNT(DISTINCT o.order_id) AS frequency, SUM(od.amount) AS monetary,
        SUM(od.profit) AS profit, SUM(od.quantity) AS quantity,
        COUNT(DISTINCT o.state) AS states, COUNT(DISTINCT od.category) AS categories
 FROM orders o JOIN order_details od ON o.order_id = od.order_id
 GROUP BY o.customer_id, o.customer_name
)
SELECT *,
       CAST(julianday((SELECT MAX(order_date) FROM orders)) - julianday(last_order) + 1 AS INTEGER) AS recency,
       CASE WHEN frequency > 0 THEN monetary * 1.0 / frequency ELSE 0 END AS avg_order_value,
       CASE WHEN monetary != 0 THEN profit * 100.0 / monetary ELSE 0 END AS profit_margin_pct
FROM customer_summary
"""

def build_customer_features() -> pd.DataFrame:
    with engine.connect() as conn:
        df = pd.read_sql(text(RFM_QUERY), conn)
    if df.empty:
        raise ValueError("No customer features available. Run ingestion first.")
    return df

def save_features(df: pd.DataFrame) -> Path:
    path = settings.processed_data_dir / "customer_features.csv"
    df.to_csv(path, index=False)
    return path

if __name__ == "__main__":
    save_features(build_customer_features())
