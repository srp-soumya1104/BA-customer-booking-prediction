import sys
from pathlib import Path
import pandas as pd
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from optimizer import BasketItem, calculate_assignment_cost, optimise_basket
from generate_data import build_data

@pytest.fixture(scope="module")
def offers():
    return build_data()

def test_synthetic_data_shape_and_products(offers):
    assert len(offers) == 45
    assert offers.product_id.nunique() == 15
    assert offers.platform.nunique() == 3

def test_optimizer_returns_each_basket_product(offers):
    allocation, summary = optimise_basket(offers, ["P001", "P003", "P005"])
    assert set(allocation.product_id) == {"P001", "P003", "P005"}
    assert summary["total_cost"] > 0

def test_discount_and_shipping_math():
    row = pd.DataFrame([{"listed_price": 1000, "discount_pct": 10, "shipping_fee": 50,
        "free_shipping_min": 2000, "coupon_code": "", "coupon_pct": 0,
        "coupon_min_spend": 0, "coupon_max_discount": 0}])
    assert calculate_assignment_cost(row) == {"items_subtotal": 900.0, "coupon_discount": 0.0, "shipping": 50.0, "total_cost": 950.0}

def test_invalid_quantity_rejected(offers):
    with pytest.raises(ValueError):
        optimise_basket(offers, [BasketItem("P001", 0)])

def test_missing_stock_rejected(offers):
    altered = offers.copy()
    altered.loc[altered.product_id == "P001", "in_stock"] = False
    with pytest.raises(ValueError):
        optimise_basket(altered, ["P001"])
