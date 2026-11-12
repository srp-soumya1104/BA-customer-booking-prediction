"""Generate deterministic synthetic e-commerce offer data for the project demo."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PRODUCTS = [
    ("P001", "Wireless Mouse", "Electronics", 799),
    ("P002", "Mechanical Keyboard", "Electronics", 2499),
    ("P003", "USB-C Hub", "Electronics", 1599),
    ("P004", "Bluetooth Speaker", "Electronics", 1899),
    ("P005", "Water Bottle", "Home", 499),
    ("P006", "Desk Lamp", "Home", 1199),
    ("P007", "Notebook Set", "Stationery", 299),
    ("P008", "Backpack", "Fashion", 1499),
    ("P009", "Running Shoes", "Fashion", 2999),
    ("P010", "Cotton T-shirt", "Fashion", 699),
    ("P011", "Cookware Set", "Home", 2199),
    ("P012", "Fitness Band", "Electronics", 3499),
    ("P013", "Coffee Mug", "Home", 349),
    ("P014", "Power Bank", "Electronics", 1299),
    ("P015", "Sunglasses", "Fashion", 999),
]
PLATFORMS = ["ShopKart", "MegaMart", "QuickBuy"]


def build_data(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for pid, name, category, base in PRODUCTS:
        for platform in PLATFORMS:
            multiplier = {"ShopKart": 1.00, "MegaMart": 0.97, "QuickBuy": 1.03}[platform]
            price = round(base * multiplier * rng.uniform(0.93, 1.08), 2)
            discount_pct = int(rng.choice([0, 5, 8, 10, 12, 15, 20], p=[.10,.10,.15,.20,.15,.20,.10]))
            shipping = round(float(rng.choice([0, 0, 0, 39, 49, 59, 79])), 2)
            free_shipping_min = float(rng.choice([0, 499, 999, 1499]))
            coupon_code, coupon_pct, coupon_min = "", 0, 0.0
            if rng.random() < 0.63:
                coupon_code = f"{platform[:2].upper()}{int(rng.integers(10, 90))}SAVE"
                coupon_pct = int(rng.choice([5, 7, 10, 12]))
                coupon_min = float(rng.choice([499, 999, 1499, 1999]))
            coupon_cap = float(rng.choice([100, 150, 200, 250])) if coupon_code else 0.0
            stock = bool(rng.random() > 0.045)
            delivery_days = int(rng.integers(1, 8))
            rows.append({
                "product_id": pid, "product_name": name, "category": category,
                "platform": platform, "listed_price": price,
                "discount_pct": discount_pct, "shipping_fee": shipping,
                "free_shipping_min": free_shipping_min,
                "coupon_code": coupon_code, "coupon_pct": coupon_pct,
                "coupon_min_spend": coupon_min, "coupon_max_discount": coupon_cap,
                "in_stock": stock, "delivery_days": delivery_days,
                "currency": "INR", "data_type": "synthetic_demo"
            })
    df = pd.DataFrame(rows)
    DATA.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA / "offers.csv", index=False)
    return df


if __name__ == "__main__":
    df = build_data()
    print(f"Generated {len(df)} synthetic offers at data/offers.csv")
