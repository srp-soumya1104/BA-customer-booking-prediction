"""Basket-level cost calculation and platform allocation optimisation."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Iterable
import pandas as pd

REQUIRED = {
    "product_id", "product_name", "platform", "listed_price", "discount_pct",
    "shipping_fee", "free_shipping_min", "coupon_code", "coupon_pct",
    "coupon_min_spend", "coupon_max_discount", "in_stock"
}

@dataclass(frozen=True)
class BasketItem:
    product_id: str
    quantity: int = 1


def validate_offers(offers: pd.DataFrame) -> None:
    missing = REQUIRED - set(offers.columns)
    if missing:
        raise ValueError(f"Offers data is missing columns: {sorted(missing)}")
    if (offers["listed_price"] < 0).any():
        raise ValueError("listed_price cannot be negative")
    if not offers["discount_pct"].between(0, 100).all():
        raise ValueError("discount_pct must be between 0 and 100")


def _net_item_price(row) -> float:
    return float(row.listed_price) * (1 - float(row.discount_pct) / 100)


def calculate_assignment_cost(selected: pd.DataFrame) -> dict:
    """Calculate cost for a set of products bought from one platform."""
    if selected.empty:
        return {"items_subtotal": 0.0, "coupon_discount": 0.0, "shipping": 0.0, "total_cost": 0.0}
    subtotal = sum(_net_item_price(r) for r in selected.itertuples(index=False))
    coupon_rows = selected[selected["coupon_code"].fillna("").astype(str).str.len() > 0]
    coupon_discount = 0.0
    for r in coupon_rows.itertuples(index=False):
        if subtotal >= float(r.coupon_min_spend):
            candidate = min(subtotal * float(r.coupon_pct) / 100, float(r.coupon_max_discount))
            coupon_discount = max(coupon_discount, candidate)
    shipping_fee = float(selected["shipping_fee"].max())
    free_shipping_min = float(selected["free_shipping_min"].max())
    shipping = 0.0 if subtotal >= free_shipping_min else shipping_fee
    return {
        "items_subtotal": round(subtotal, 2),
        "coupon_discount": round(coupon_discount, 2),
        "shipping": round(shipping, 2),
        "total_cost": round(subtotal - coupon_discount + shipping, 2),
    }


def optimise_basket(offers: pd.DataFrame, basket: Iterable[BasketItem | dict | str], max_platforms: int = 3) -> tuple[pd.DataFrame, dict]:
    """Find minimum-cost in-stock offer allocation using exhaustive enumeration.

    Suitable for the small demonstration catalogue. For large baskets, replace
    exhaustive enumeration with integer programming or a pruned search.
    """
    validate_offers(offers)
    if max_platforms < 1:
        raise ValueError("max_platforms must be at least one")
    items = []
    for item in basket:
        if isinstance(item, str):
            items.append(BasketItem(item, 1))
        elif isinstance(item, dict):
            items.append(BasketItem(str(item["product_id"]), int(item.get("quantity", 1))))
        else:
            items.append(item)
    if not items:
        raise ValueError("Basket must contain at least one item")
    if any(i.quantity < 1 for i in items):
        raise ValueError("Every quantity must be at least one")

    choices = []
    for item in items:
        available = offers[(offers.product_id == item.product_id) & offers.in_stock.astype(bool)].copy()
        if available.empty:
            raise ValueError(f"No in-stock offer found for product_id={item.product_id}")
        available["quantity"] = item.quantity
        choices.append([row for _, row in available.iterrows()])

    candidates = []
    for combination in product(*choices):
        assignment = pd.DataFrame(combination).reset_index(drop=True)
        if assignment.platform.nunique() > max_platforms:
            continue
        total, breakdown = 0.0, []
        for platform, group in assignment.groupby("platform"):
            quantity_adjusted = group.copy()
            quantity_adjusted["listed_price"] *= quantity_adjusted["quantity"]
            cost = calculate_assignment_cost(quantity_adjusted)
            total += cost["total_cost"]
            breakdown.append({"platform": platform, **cost})
        assignment["net_unit_price"] = assignment.listed_price * (1 - assignment.discount_pct / 100)
        candidates.append((round(total, 2), assignment, breakdown))

    if not candidates:
        raise ValueError("No feasible platform allocation found")
    candidates.sort(key=lambda x: (x[0], x[1].platform.nunique(), tuple(x[1].platform)))
    best_total, best, breakdown = candidates[0]
    best = best[["product_id", "product_name", "platform", "quantity", "listed_price", "discount_pct", "net_unit_price", "delivery_days", "coupon_code"]].copy()
    best["net_unit_price"] = best["net_unit_price"].round(2)
    return best, {
        "total_cost": best_total,
        "platform_count": len(breakdown),
        "platform_breakdown": breakdown,
        "allocations_evaluated": len(candidates),
    }


def compare_strategies(offers: pd.DataFrame, basket: list[BasketItem | dict | str]) -> pd.DataFrame:
    """Compare best single-platform strategy with unrestricted split basket."""
    records = []
    for platform in sorted(offers.platform.unique()):
        try:
            _, result = optimise_basket(offers[offers.platform == platform], basket, max_platforms=1)
            records.append({"strategy": f"All items from {platform}", "total_cost": result["total_cost"], "platform_count": 1})
        except ValueError:
            continue
    _, split = optimise_basket(offers, basket, max_platforms=len(offers.platform.unique()))
    records.append({"strategy": "Optimised split basket", "total_cost": split["total_cost"], "platform_count": split["platform_count"]})
    out = pd.DataFrame(records).sort_values("total_cost").reset_index(drop=True)
    single_costs = out.loc[out.strategy.str.startswith("All items"), "total_cost"]
    if single_costs.empty:
        raise ValueError("No single-platform strategy can fulfil the complete basket")
    best_single = single_costs.min()
    out["saving_vs_best_single"] = (best_single - out.total_cost).round(2)
    out["saving_pct"] = (out.saving_vs_best_single / best_single * 100).round(2)
    return out
