# SQL layer

Load the generated offer dataset into SQLite by running `python src/load_sqlite.py` from the project directory.

This creates `outputs/basket_economics.sqlite` and exports:

- `outputs/sql_platform_overview.csv`
- `outputs/sql_cheapest_offer_by_product.csv`

Reusable SQLite / MySQL 8+ queries are in `queries.sql`. The cheapest-offer query ranks in-stock discounted item prices by product. Coupon qualification must be calculated at the final platform-order subtotal; the Python optimiser handles the simplified basket-level coupon and shipping assumptions.
