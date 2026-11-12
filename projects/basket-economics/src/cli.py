"""Simple command-line interface for custom baskets."""
import argparse
from pathlib import Path
import pandas as pd
from optimizer import BasketItem, optimise_basket

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="Optimise a product basket across shopping platforms")
    parser.add_argument("--items", nargs="+", required=True, help="Product IDs, e.g. P001 P003 P005")
    parser.add_argument("--max-platforms", type=int, default=3)
    args = parser.parse_args()
    offers = pd.read_csv(ROOT / "data" / "offers.csv")
    allocation, result = optimise_basket(offers, [BasketItem(pid) for pid in args.items], args.max_platforms)
    print(allocation.to_string(index=False))
    print("\nCost summary:", result)

if __name__ == "__main__":
    main()
