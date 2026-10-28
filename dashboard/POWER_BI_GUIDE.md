# Power BI dashboard guide

Import `data/processed/customer_segments.csv` after running the Python pipeline.

## Data model
For a simple portfolio project, one customer-level table is enough for the segmentation pages. If you want a stronger model, also import `merged_orders_cleaned.csv` and create:

- `Customers` → one row per CustomerName
- `Orders` → one row per order-detail record
- Relationship: Customers[CustomerName] → Orders[CustomerName]

Keep the model simple. Do not create tables just to make the project look complicated.

## Page 1 — Executive overview
Cards:
- Total Revenue
- Total Profit
- Customers
- Average Order Value
- Profit Margin %

Visuals:
- Monthly revenue trend (use the transaction table)
- Revenue by RFM segment
- Top 10 customers by revenue
- Revenue vs profit by category

## Page 2 — Customer segmentation
Visuals:
- Scatter: Recency vs Monetary; size = Frequency
- Column chart: customers by RFM segment
- Bar chart: revenue by segment
- Detail table: Customer, Recency, Frequency, Revenue, Profit, RFM Segment, Cluster

## Page 3 — Retention opportunities
Use the RFM segment `High Value - At Risk` as a **review list**, not as proof that customers will churn.

Visuals:
- Count of high-value at-risk customers
- Revenue represented by that group
- Table of customers sorted by historical revenue
- State/category breakdown if the transaction table is loaded

## Suggested DAX
```DAX
Total Revenue = SUM(customer_segments[monetary])
Total Profit = SUM(customer_segments[profit])
Customer Count = DISTINCTCOUNT(customer_segments[CustomerName])
Average Order Value = DIVIDE([Total Revenue], SUM(customer_segments[frequency]))
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
At Risk Revenue = CALCULATE([Total Revenue], customer_segments[rfm_segment] = "High Value - At Risk")
At Risk Customers = CALCULATE([Customer Count], customer_segments[rfm_segment] = "High Value - At Risk")
```

## Design rule
Keep the dashboard restrained: 4–6 useful visuals per page, clear titles, consistent number formatting, and no decorative charts that do not answer a business question.

## Important
This repository does not contain a `.pbix` file because Power BI Desktop is a local Windows application. Build the dashboard using this guide, then save the resulting `.pbix` in your own portfolio repository if you want to showcase it.
