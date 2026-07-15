"""
Generates a SYNTHETIC sample dataset that mirrors the column schema and
class imbalance of the real `customer_booking.csv` file provided in the
British Airways "Data Science" job simulation on Forage.

This is NOT the real Forage dataset — it does not exist in this environment.
It exists so the notebook in this repo is runnable end-to-end out of the box.
For your actual simulation results, replace data/sample_customer_booking.csv
with the real customer_booking.csv you downloaded from Forage (same column
names, so no code changes needed).
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 6000

ROUTES = [
    "AKLKUL", "AKLDEL", "AKLHGH", "KULAKL", "DELAKL", "PENTPE", "ICNSIN",
    "SINICN", "KIXAKL", "PVGAKL", "HGHAKL", "TPEPEN", "SGNAKL", "AKLSGN",
    "BOMDXB", "DXBBOM", "SYDAKL", "AKLSYD", "NRTAKL", "AKLNRT",
]
ORIGINS = [
    "New Zealand", "Australia", "India", "China", "Malaysia", "South Korea",
    "Japan", "Singapore", "Indonesia", "Taiwan", "Thailand", "Vietnam",
    "United Kingdom", "United States", "United Arab Emirates", "Hong Kong",
]
ORIGIN_P = np.array([22, 18, 10, 8, 8, 6, 6, 5, 5, 3, 3, 2, 2, 1, 1, 0.5])
ORIGIN_P = ORIGIN_P / ORIGIN_P.sum()

df = pd.DataFrame({
    "num_passengers": rng.integers(1, 6, N),
    "sales_channel": rng.choice(["Internet", "Mobile"], N, p=[0.88, 0.12]),
    "trip_type": rng.choice(["RoundTrip", "OneWay", "CircleTrip"], N, p=[0.82, 0.14, 0.04]),
    "purchase_lead": rng.integers(0, 500, N),
    "length_of_stay": rng.integers(0, 400, N),
    "flight_hour": rng.integers(0, 24, N),
    "flight_day": rng.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], N),
    "route": rng.choice(ROUTES, N),
    "booking_origin": rng.choice(ORIGINS, N, p=ORIGIN_P),
    "wants_extra_baggage": rng.choice([0, 1], N, p=[0.67, 0.33]),
    "wants_preferred_seat": rng.choice([0, 1], N, p=[0.70, 0.30]),
    "wants_in_flight_meals": rng.choice([0, 1], N, p=[0.72, 0.28]),
    "flight_duration": rng.uniform(1, 16, N).round(2),
})

# Bake in real signal so the model has genuine patterns to learn
# (mirrors what tends to show up in the actual simulation dataset:
# add-on purchases and trip type are informative; most raw noise dominates).
logit = (
    -3.55
    + 1.55 * df["wants_extra_baggage"]
    + 1.05 * df["wants_preferred_seat"]
    + 0.80 * df["wants_in_flight_meals"]
    + 0.60 * (df["trip_type"] == "RoundTrip")
    + 0.25 * (df["sales_channel"] == "Internet")
    - 0.0018 * df["purchase_lead"]
    + 0.0012 * df["length_of_stay"]
    + rng.normal(0, 0.55, N)
)
p = 1 / (1 + np.exp(-logit))
df["booking_complete"] = rng.binomial(1, p)

out_path = "/home/claude/ba-customer-booking-prediction/data/sample_customer_booking.csv"
df.to_csv(out_path, index=False)

print(f"Rows: {len(df)}")
print(f"Positive rate (booking_complete=1): {df['booking_complete'].mean():.3f}")
print(f"Saved to: {out_path}")
