"""Estimate where conversion improvement could recover the most purchases."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "ecommerce_funnel.db"
OUTPUT = ROOT / "data" / "opportunity_priorities.csv"

QUERY = """
WITH funnel_flags AS (
    SELECT
        user_id,
        device_type,
        traffic_source,
        region,
        MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS viewed_product,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_type = 'checkout_start' THEN 1 ELSE 0 END) AS started_checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM ecommerce_user_events
    GROUP BY user_id, device_type, traffic_source, region
), segments AS (
    SELECT 'Device' AS segment_type, device_type AS segment_value,
           viewed_product, added_to_cart, started_checkout, purchased
    FROM funnel_flags
    UNION ALL
    SELECT 'Traffic source', traffic_source,
           viewed_product, added_to_cart, started_checkout, purchased
    FROM funnel_flags
    UNION ALL
    SELECT 'Region', region,
           viewed_product, added_to_cart, started_checkout, purchased
    FROM funnel_flags
)
SELECT segment_type, segment_value,
       SUM(viewed_product) AS visitors,
       SUM(added_to_cart) AS add_to_carts,
       SUM(started_checkout) AS checkouts,
       SUM(purchased) AS purchases,
       ROUND(100.0 * SUM(purchased) / SUM(viewed_product), 2) AS purchase_rate
FROM segments
GROUP BY segment_type, segment_value
"""


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(QUERY, conn)

    best_rates = df.groupby("segment_type")["purchase_rate"].transform("max")
    df["best_rate_in_group"] = best_rates
    df["rate_gap_pp"] = (df["best_rate_in_group"] - df["purchase_rate"]).round(2)
    df["recoverable_purchases"] = (
        df["visitors"] * df["rate_gap_pp"] / 100
    ).round(1)
    df["priority_score"] = (
        df["recoverable_purchases"] * df["rate_gap_pp"]
    ).round(1)
    df = df.sort_values(["recoverable_purchases", "rate_gap_pp"], ascending=False)
    df.to_csv(OUTPUT, index=False)
    print(f"Opportunity analysis written to {OUTPUT}")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
