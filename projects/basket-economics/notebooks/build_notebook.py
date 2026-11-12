from pathlib import Path
import nbformat as nbf
ROOT = Path(__file__).resolve().parents[1]
nb = nbf.v4.new_notebook()
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
nb.cells = [
 nbf.v4.new_markdown_cell("# Basket Economics: Cross-Platform Shopping Cost Optimisation\n\n**Portfolio demonstration — all included offer data is synthetic.**\n\nExplore offers, calculate basket cost after discounts/coupons/shipping, and compare a single-platform purchase with an optimised split basket."),
 nbf.v4.new_markdown_cell("## 1. Setup and imports"),
 nbf.v4.new_code_cell("from pathlib import Path\nimport sys\nimport pandas as pd\nimport matplotlib.pyplot as plt\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT / 'src'))\nfrom generate_data import build_data\nfrom optimizer import BasketItem, optimise_basket, compare_strategies"),
 nbf.v4.new_markdown_cell("## 2. Load the synthetic demonstration data\n\nThe 45 rows represent fictional offers for 15 products on three fictional platforms. They are not live retailer prices."),
 nbf.v4.new_code_cell("offers_path = ROOT / 'data' / 'offers.csv'\noffers = pd.read_csv(offers_path) if offers_path.exists() else build_data()\nprint(offers.shape)\noffers.head()"),
 nbf.v4.new_markdown_cell("## 3. Data quality and offer overview"),
 nbf.v4.new_code_cell("offers.info()\nprint('Missing values:', offers.isna().sum().sum())\nprint('Duplicate product-platform pairs:', offers.duplicated(['product_id', 'platform']).sum())\ndisplay(offers.groupby('platform').agg(offers=('product_id','count'), stock_rate=('in_stock','mean'), avg_discount=('discount_pct','mean')).round(3))"),
 nbf.v4.new_code_cell("platform_avg = offers.groupby('platform', as_index=False).agg(avg_listed_price=('listed_price','mean'), avg_discount=('discount_pct','mean'))\nplatform_avg"),
 nbf.v4.new_code_cell("ax = platform_avg.plot(x='platform', y='avg_listed_price', kind='bar', legend=False, title='Average listed price by platform (synthetic)')\nax.set_ylabel('INR'); plt.tight_layout()"),
 nbf.v4.new_markdown_cell("## 4. Define a sample basket\n\nOne wireless mouse, one USB-C hub, two water bottles, and one backpack."),
 nbf.v4.new_code_cell("basket = [BasketItem('P001', 1), BasketItem('P003', 1), BasketItem('P005', 2), BasketItem('P008', 1)]\n[(x.product_id, x.quantity) for x in basket]"),
 nbf.v4.new_markdown_cell("## 5. Optimise product allocation"),
 nbf.v4.new_code_cell("allocation, summary = optimise_basket(offers, basket)\nallocation"),
 nbf.v4.new_code_cell("summary"),
 nbf.v4.new_markdown_cell("## 6. Compare purchasing strategies"),
 nbf.v4.new_code_cell("strategy = compare_strategies(offers, basket)\nstrategy"),
 nbf.v4.new_code_cell("ax = strategy.sort_values('total_cost').plot(x='strategy', y='total_cost', kind='bar', legend=False, title='Total basket cost by strategy')\nax.set_ylabel('INR'); ax.tick_params(axis='x', rotation=15); plt.tight_layout()"),
 nbf.v4.new_markdown_cell("## 7. Interpret the result\n\nThe split basket is preferable only when its final total, after platform-level shipping and coupon rules, is below the cheapest single-platform total. Results from this synthetic data are illustrative, not observed savings."),
 nbf.v4.new_code_cell("best_single = strategy[strategy.strategy.str.startswith('All items')].total_cost.min()\nsplit_cost = strategy.loc[strategy.strategy == 'Optimised split basket', 'total_cost'].iloc[0]\nprint(f'Best single-platform cost: INR {best_single:,.2f}')\nprint(f'Optimised split-basket cost: INR {split_cost:,.2f}')\nprint(f'Illustrative difference: INR {best_single-split_cost:,.2f}')"),
 nbf.v4.new_markdown_cell("## 8. Export result tables"),
 nbf.v4.new_code_cell("allocation.to_csv(ROOT / 'outputs' / 'optimised_allocation.csv', index=False)\nstrategy.to_csv(ROOT / 'outputs' / 'strategy_comparison.csv', index=False)\nprint('Saved core result tables.')"),
]
nbf.write(nb, ROOT / "notebooks" / "Basket_Economics_Analysis.ipynb")
print("Notebook created")
