# Indian E-Commerce Customer Segmentation — Production Refactor

This project converts the original notebook/CSV analysis into a reproducible, database-backed ML pipeline. The notebook remains for exploration; production logic lives under `src/`.

## Architecture
`raw CSV -> ingest.py -> SQLite/PostgreSQL -> features.py -> train.py -> segmentation.joblib -> predict.py`

## Run
1. Copy `.env.example` to `.env`.
2. Put the original `List of Orders.csv` and `Order Details.csv` files in `data/raw/`.
3. `pip install -r requirements.txt`
4. `python -m src.ingest`
5. `python -m src.train`
6. `python -m src.predict --customer-id USR-9921 --recency 4 --frequency 28 --monetary-value 4500.50`
7. `pytest`

## Honest ML claim
K-Means is unsupervised clustering. The `HIGH_VALUE_AT_RISK` / `CHURN_RISK` labels are explicit business rules, not supervised churn probabilities.
