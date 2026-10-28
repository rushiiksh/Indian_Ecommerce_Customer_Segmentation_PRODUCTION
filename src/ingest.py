import hashlib
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import delete
from src.config import settings
from src.db import SessionLocal, engine
from src.schema import Base, Order, OrderDetail

log = logging.getLogger(__name__)
ORDERS_FILE = "List of Orders.csv"
DETAILS_FILE = "Order Details.csv"

def make_customer_id(name: str) -> str:
    normalized = " ".join(str(name).strip().lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]

def _read(path: Path, required: set[str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
    return df

def ingest() -> None:
    orders = _read(settings.raw_data_dir / ORDERS_FILE, {"Order ID","Order Date","CustomerName","State"})
    details = _read(settings.raw_data_dir / DETAILS_FILE, {"Order ID","Amount","Profit","Quantity","Category","Sub-Category"})
    orders["Order Date"] = pd.to_datetime(orders["Order Date"], errors="coerce", dayfirst=True)
    orders = orders.dropna(subset=["Order ID","Order Date","CustomerName"]).copy()
    orders["Order ID"] = orders["Order ID"].astype(str).str.strip()
    orders["customer_id"] = orders["CustomerName"].map(make_customer_id)
    if orders["Order ID"].duplicated().any():
        raise ValueError("Duplicate Order ID values found in orders source")
    for c in ["Amount","Profit","Quantity"]:
        details[c] = pd.to_numeric(details[c], errors="coerce")
    details = details.dropna(subset=["Order ID"]).copy()
    details["Order ID"] = details["Order ID"].astype(str).str.strip()
    details[["Amount","Profit","Quantity"]] = details[["Amount","Profit","Quantity"]].fillna(0)
    unknown = set(details["Order ID"]) - set(orders["Order ID"])
    if unknown:
        raise ValueError(f"Found {len(unknown)} order-detail rows without a matching order")
    Base.metadata.create_all(engine)
    with SessionLocal.begin() as session:
        session.execute(delete(OrderDetail))
        session.execute(delete(Order))
        session.add_all([Order(order_id=r["Order ID"], order_date=r["Order Date"].date(), customer_id=r["customer_id"], customer_name=str(r["CustomerName"]).strip(), state=r["State"]) for _,r in orders.iterrows()])
        session.add_all([OrderDetail(order_id=r["Order ID"], amount=float(r["Amount"]), profit=float(r["Profit"]), quantity=int(r["Quantity"]), category=r["Category"], sub_category=r["Sub-Category"]) for _,r in details.iterrows()])
    log.info("Ingested %d orders and %d detail rows", len(orders), len(details))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    ingest()
