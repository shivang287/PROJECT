import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import joblib
from pathlib import Path


# ==========================================
# 1. GENERATE DEMO HISTORICAL DATA
# ==========================================

np.random.seed(42)

dates = pd.date_range(
    start="2026-01-01",
    end="2026-08-25",
    freq="D"
)

data = []

base_demand = 3800


for date in dates:

    # Seasonal effect
    seasonal_effect = (
        500 * np.sin(
            2 * np.pi * date.dayofyear / 365
        )
    )

    # Weekend effect
    weekend_effect = (
        250
        if date.dayofweek >= 5
        else 0
    )

    # Random market variation
    random_effect = np.random.normal(
        0,
        180
    )

    demand = (
        base_demand
        + seasonal_effect
        + weekend_effect
        + random_effect
    )

    demand = max(
        2000,
        round(demand)
    )

    # Simulated market price
    price = (
        24
        + np.random.normal(0, 1.5)
    )

    data.append({
        "date": date,
        "product": "Tomato",
        "location": "Delhi NCR",
        "demand_kg": demand,
        "price_per_kg": round(price, 2)
    })


df = pd.DataFrame(data)


# Save historical data

Path("data").mkdir(
    exist_ok=True
)

df.to_csv(
    "data/demand_history.csv",
    index=False
)


print("Historical dataset created.")
print(f"Records: {len(df)}")


# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================

df["date"] = pd.to_datetime(
    df["date"]
)

df["day_of_year"] = (
    df["date"].dt.dayofyear
)

df["month"] = (
    df["date"].dt.month
)

df["day_of_week"] = (
    df["date"].dt.dayofweek
)

df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)


# ==========================================
# 3. FEATURES & TARGET
# ==========================================

features = [
    "day_of_year",
    "month",
    "day_of_week",
    "is_weekend",
    "price_per_kg"
]

X = df[features]

y = df["demand_kg"]


# ==========================================
# 4. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# 5. TRAIN MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# ==========================================
# 6. MODEL EVALUATION
# ==========================================

predictions = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(
    f"Mean Absolute Error: {mae:.2f} kg"
)


# ==========================================
# 7. SAVE MODEL
# ==========================================

Path("models").mkdir(
    exist_ok=True
)

joblib.dump(
    model,
    "models/demand_model.pkl"
)

print(
    "Model saved to models/demand_model.pkl"
)