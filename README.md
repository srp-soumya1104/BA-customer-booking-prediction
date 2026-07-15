# Predictive Modeling for Customer Booking – British Airways

Predicts whether a customer will complete a flight booking, based on data from
the British Airways **Data Science job simulation** on [Forage](https://www.theforage.com/).

**Tools:** Pandas · Scikit-learn · LightGBM · imbalanced-learn (SMOTE) · Matplotlib · Seaborn

## What this project does

1. Explores a customer booking dataset (channel, trip type, lead time, add-ons, route, etc.)
2. Encodes categorical features (frequency encoding for high-cardinality columns, one-hot for the rest)
3. Balances the heavily skewed target class (~85/15) with **SMOTE**, applied to the training set only
4. Trains a **LightGBM** classifier to predict `booking_complete`
5. Evaluates with a classification report, ROC-AUC, confusion matrix, and threshold tuning
6. Visualizes which features drive booking completion

## Results at a glance

On the bundled sample dataset: **ROC-AUC ≈ 0.70**, with `wants_extra_baggage`,
`wants_preferred_seat`, and `wants_in_flight_meals` (the paid add-ons) standing out
as the strongest predictors — customers who engage with extras are meaningfully
more likely to complete their booking. Full metrics and charts are in the notebook.

## Project structure

```
├── data/
│   ├── sample_customer_booking.csv   # synthetic sample data (see data/README.md)
│   └── README.md
├── notebook/
│   └── BA_booking_prediction_analysis.ipynb   # full walkthrough, pre-run with real outputs
├── src/
│   ├── generate_sample_data.py       # (re)generates the synthetic sample dataset
│   ├── build_notebook.py             # builds the notebook from its cell definitions
│   └── train_model.py                # same pipeline as a plain script
├── figures/                          # exported chart PNGs
├── requirements.txt
└── README.md
```

## ⚠️ About the data

This repo ships with `data/sample_customer_booking.csv` — a **synthetically
generated** dataset built to match the real Forage file's column names and
class imbalance, so the notebook runs immediately with no setup. **It is not
the real Forage dataset**, and its exact numbers won't match your simulation
results.

To reproduce your own results: download `customer_booking.csv` from the
Forage task and drop it into `data/` under the same filename (or update the
path in the notebook's first `read_csv` call). Same column names, so nothing
else needs to change. See `data/README.md` for details.

## Getting started

```bash
git clone <your-repo-url>
cd ba-customer-booking-prediction
pip install -r requirements.txt
jupyter notebook notebook/BA_booking_prediction_analysis.ipynb
```

Or run it as a plain script:

```bash
python src/train_model.py
```

**Note:** `lightgbm` and `imbalanced-learn` need a real internet connection to
install and aren't available in every sandboxed environment. The code
automatically falls back to `GradientBoostingClassifier` and a small
from-scratch SMOTE implementation if either is missing, so it always runs —
but install `requirements.txt` on your own machine to use the real
LightGBM + SMOTE this project is built around.

## Possible next steps

- Hyperparameter tuning (`GridSearchCV`, Optuna)
- Target encoding for `route` / `booking_origin` instead of frequency encoding
- Compare against XGBoost / CatBoost
- Deploy as a simple API (FastAPI/Flask) that scores a booking in real time

## License

MIT — see `LICENSE`.
