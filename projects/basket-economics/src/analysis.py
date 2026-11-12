"""Run the complete basket economics analysis and export tables/figures."""
from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from generate_data import build_data
from optimizer import BasketItem, compare_strategies, optimise_basket

DATA, OUT = ROOT / "data", ROOT / "outputs"
FIG = OUT / "figures"


def run():
    OUT.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)
    offers_path = DATA / "offers.csv"
    offers = pd.read_csv(offers_path) if offers_path.exists() else build_data()
    basket = [BasketItem("P001", 1), BasketItem("P003", 1), BasketItem("P005", 2), BasketItem("P008", 1)]
    allocation, summary = optimise_basket(offers, basket)
    strategy = compare_strategies(offers, basket)
    allocation.to_csv(OUT / "optimised_allocation.csv", index=False)
    strategy.to_csv(OUT / "strategy_comparison.csv", index=False)
    pd.DataFrame(summary["platform_breakdown"]).to_csv(OUT / "platform_cost_breakdown.csv", index=False)
    offer_summary = offers.groupby("platform").agg(
        mean_listed_price=("listed_price", "mean"), mean_discount_pct=("discount_pct", "mean"),
        in_stock_rate=("in_stock", "mean"), mean_delivery_days=("delivery_days", "mean"),
    ).reset_index()
    offer_summary.to_csv(OUT / "platform_offer_summary.csv", index=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(strategy.strategy, strategy.total_cost)
    ax.set_title("Basket cost by purchasing strategy (synthetic demo)")
    ax.set_ylabel("Total cost (INR)")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout(); fig.savefig(FIG / "strategy_comparison.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(offer_summary.platform, offer_summary.mean_listed_price)
    ax.set_title("Average listed price by platform (synthetic demo)")
    ax.set_ylabel("Average listed price (INR)")
    fig.tight_layout(); fig.savefig(FIG / "average_platform_price.png", dpi=180); plt.close(fig)
    best_single = strategy[strategy.strategy.str.startswith("All items")].total_cost.min()
    split_cost = float(strategy.loc[strategy.strategy == "Optimised split basket", "total_cost"].iloc[0])
    saving = round(best_single - split_cost, 2)
    print("\nBASKET ECONOMICS — DEMO RUN")
    print("Data type: SYNTHETIC DEMO — not live marketplace data")
    print(f"Products in basket: {len(basket)} (5 units)")
    print(f"Best single-platform cost: INR {best_single:,.2f}")
    print(f"Optimised split-basket cost: INR {split_cost:,.2f}")
    print(f"Illustrative saving: INR {saving:,.2f} ({saving / best_single * 100:.2f}%)")
    print(f"Winning allocation uses {summary['platform_count']} platform(s)")
    print("Outputs saved to outputs/")
    return strategy, allocation, summary

if __name__ == "__main__":
    run()
