# Basket Economics: Cross-Platform Shopping Cost Optimisation

**Author:** Soumya Ranjan Pradhan  
**Stack:** Python · SQL · Pandas · NumPy · Matplotlib · Excel / Power BI  
**Status:** Reproducible portfolio project using synthetic demonstration data

## 1. Business problem

Comparing item prices alone can lead to the wrong purchasing decision. Final checkout cost also depends on item discounts, order-level coupons, coupon caps and minimum spends, shipping fees, free-shipping thresholds, and stock availability. The cheapest unit price does not always produce the cheapest complete basket.

This project compares buying the entire basket from one marketplace with splitting it across marketplaces. It recommends the minimum-cost feasible allocation and shows the cost components behind the recommendation.

## 2. Project objectives

- Compare the same product's offers across multiple marketplaces.
- Calculate discounted line prices and basket-level coupon eligibility.
- Apply coupon caps and shipping / free-shipping thresholds.
- Exclude out-of-stock offers.
- Find the least-cost allocation across one or more platforms.
- Quantify the difference between the best single-platform basket and an optimised split basket.
- Export analysis tables, charts, a formatted Excel dashboard, and SQL summaries.

## 3. Cost methodology

For listed unit price P and discount percentage d:

**Discounted unit price = P × (1 − d / 100)**

For a platform order with discounted subtotal S, coupon percentage c, coupon cap K, and minimum spend M:

**Coupon discount = min(S × c / 100, K)** when S ≥ M; otherwise the coupon discount is zero.

Shipping is zero when the order subtotal reaches the free-shipping threshold; otherwise the platform shipping fee applies.

**Order total = S − coupon discount + shipping**

The optimiser enumerates the in-stock platform choice for each requested product, calculates each platform order independently, and selects the lowest basket total. For this compact sample catalogue, exhaustive enumeration is exact and auditable. A larger catalogue should use pruning or an integer-programming solver.

**Demonstration rule assumption:** for a platform order, the engine uses the strictest (largest) free-shipping threshold and the highest valid coupon benefit found among the selected offer rows. Real marketplace rules may include coupon exclusions, seller-level shipping, coupon stacking restrictions, payment offers, taxes, and additional fees. Validate actual rule semantics before using live data.

## 4. Data and integrity

The data generator creates 45 synthetic product-offer rows: 15 fictional products × 3 fictional platforms. Prices, discounts, shipping, coupon rules, stock status, and delivery estimates are fictional and use a fixed random seed. **This is a method demonstration, not scraped marketplace data or proof of real customer savings.**

Run the generator before analysis: python src/generate_data.py. See data/README.md for the field dictionary.

## 5. Project structure

- data/ — generator output and dataset documentation.
- notebooks/ — analysis notebook and notebook builder.
- outputs/ — reproducible CSV tables, figures, Excel workbook, and SQLite database.
- src/ — data generation, optimiser, analysis, CLI, dashboard builder, and SQLite loader.
- sql/ — reusable SQL queries and documentation.
- tests/ — automated checks for data and cost calculations.
- .github/workflows/basket-economics.yml — GitHub Actions validation workflow.

## 6. Run locally

Python 3.10+ is recommended. The project is inside the existing repository's projects/basket-economics folder.

1. Clone the repository: git clone https://github.com/srp-soumya1104/BA-customer-booking-prediction.git
2. Change directory: cd BA-customer-booking-prediction/projects/basket-economics
3. Create a virtual environment: python -m venv .venv
4. Activate it (Windows PowerShell: .venv\Scripts\Activate.ps1; macOS/Linux: source .venv/bin/activate).
5. Install packages: pip install -r requirements.txt
6. Generate data: python src/generate_data.py
7. Run analysis: python src/analysis.py
8. Build the Excel dashboard: python src/make_dashboard.py
9. Load and query SQLite: python src/load_sqlite.py
10. Run tests: pytest -q

Open outputs/Basket_Economics_Dashboard.xlsx in Excel. For Power BI, use Get Data → Text/CSV or Excel Workbook and load strategy_comparison.csv, platform_cost_breakdown.csv, optimised_allocation.csv, and platform_offer_summary.csv.

## 7. Custom basket

Product IDs in the generated data are P001 through P015. Example:

python src/cli.py --items P001 P003 P005 P008 --max-platforms 3

The CLI prints the recommended item-to-platform assignment and cost summary.

## 8. SQL analysis

The SQLite loader creates a table named offers and exports a cheapest in-stock offer per product plus platform availability and discount summaries. Reusable SQLite / MySQL 8+ queries are in sql/queries.sql.

The SQL cheapest-item query compares discounted item prices only. Coupon qualification must be checked against the final order subtotal; the Python optimiser handles the simplified basket-level coupon and shipping assumptions described above.

## 9. Dashboard recommendations

Build the following Power BI visuals from the exported tables:

1. KPI cards: optimised basket cost, best single-platform cost, absolute saving, saving percentage, and number of platforms.
2. Strategy comparison: bar chart of total basket cost by purchasing strategy.
3. Platform contribution: chart using platform cost breakdown.
4. Product allocation: product, selected platform, discounted unit cost, and delivery days.
5. Offer landscape: average discount and in-stock rate by platform.
6. Slicers: category, platform, product, and in-stock status.

The Excel workbook is a starter dashboard, not a Power BI .pbix file. Binary presentation outputs are generated locally by the scripts.

## 10. Limitations and next steps

- Synthetic data only; no current marketplace prices, live APIs, or web scraping are used.
- Coupon eligibility is modelled at platform-order level and simplified as noted above.
- Payment promotions, loyalty rewards, seller-level splitting, returns, taxes, convenience charges, and delivery-speed preferences are not included.
- Exhaustive search suits the small demonstration basket; large baskets need a scalable optimisation method.

Next steps: ingest permitted real offer data with timestamps; normalise product matching; model seller-specific shipping and coupon exclusions; add delivery-time and reliability constraints; persist offers in MySQL; schedule refreshes; deploy a Streamlit or FastAPI interface; and build a Power BI report.

## 11. Responsible use

Collect data only through permitted APIs or sources whose terms allow it. Disclose data age and source, store timestamps, and do not represent indicative prices as guaranteed checkout prices. Confirm final prices and coupon terms at retailer checkout.

## License

MIT. See LICENSE.
