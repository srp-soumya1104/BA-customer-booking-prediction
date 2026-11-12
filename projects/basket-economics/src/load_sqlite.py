"""Load offer data into SQLite and export reusable SQL summaries."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data" / "offers.csv", ROOT / "outputs"


def run():
    OUT.mkdir(exist_ok=True)
    offers = pd.read_csv(DATA)
    db_path = OUT / "basket_economics.sqlite"
    with sqlite3.connect(db_path) as conn:
        offers.to_sql("offers", conn, if_exists="replace", index=False)
        overview = pd.read_sql_query("""SELECT platform, COUNT(*) AS listed_offers,
            SUM(CASE WHEN in_stock = 1 THEN 1 ELSE 0 END) AS available_offers,
            ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
            ROUND(100.0 * SUM(CASE WHEN in_stock = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS stock_rate_pct
            FROM offers GROUP BY platform ORDER BY platform""", conn)
        cheapest = pd.read_sql_query("""WITH ranked AS (
            SELECT product_id, product_name, platform,
                ROUND(listed_price * (1.0 - discount_pct / 100.0), 2) AS discounted_price,
                ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY listed_price * (1.0 - discount_pct / 100.0), platform) AS rn
            FROM offers WHERE in_stock = 1)
            SELECT product_id, product_name, platform, discounted_price FROM ranked WHERE rn = 1 ORDER BY product_id""", conn)
    overview.to_csv(OUT / "sql_platform_overview.csv", index=False)
    cheapest.to_csv(OUT / "sql_cheapest_offer_by_product.csv", index=False)
    print(f"SQLite database: {db_path.relative_to(ROOT)}")
    print("Exported SQL summary tables to outputs/")

if __name__ == "__main__":
    run()
