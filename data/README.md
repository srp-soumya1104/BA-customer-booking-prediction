# Data

## `sample_customer_booking.csv`

A **synthetically generated** dataset (6,000 rows), created by
`src/generate_sample_data.py`. It matches the column schema and roughly
mirrors the class imbalance (~85% not completed / ~15% completed) of the real
`customer_booking.csv` file provided in the British Airways Data Science job
simulation on Forage.

It exists so this repository runs end-to-end without needing any external
file. **It is not real customer data, and it is not the Forage dataset** —
treat any numbers/results from it as illustrative only.

Columns:

| Column | Description |
|---|---|
| `num_passengers` | Number of passengers on the booking |
| `sales_channel` | `Internet` or `Mobile` |
| `trip_type` | `RoundTrip`, `OneWay`, or `CircleTrip` |
| `purchase_lead` | Days between booking and departure |
| `length_of_stay` | Length of stay at destination, in days |
| `flight_hour` | Scheduled departure hour (0–23) |
| `flight_day` | Scheduled departure day of week |
| `route` | Origin–destination airport pair code |
| `booking_origin` | Country the booking was made from |
| `wants_extra_baggage` | 1 if extra baggage was requested |
| `wants_preferred_seat` | 1 if a preferred seat was requested |
| `wants_in_flight_meals` | 1 if an in-flight meal was requested |
| `flight_duration` | Scheduled flight duration, in hours |
| `booking_complete` | Target: 1 if the booking was completed |

## Using your real Forage data

1. Complete the British Airways Data Science job simulation on Forage and
   download the real `customer_booking.csv`.
2. Place it in this `data/` folder.
3. In the notebook's data-loading cell, point `pd.read_csv(...)` at your file
   instead of `sample_customer_booking.csv`. Column names match, so the rest
   of the notebook runs unchanged.
4. Re-run all cells to get your actual results.
