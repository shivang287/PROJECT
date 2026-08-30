import pandas as pd
import joblib


MODEL_PATH = "models/demand_model.pkl"
DATA_PATH = "data/demand_history.csv"


def load_model():

    return joblib.load(
        MODEL_PATH
    )


def load_history():

    df = pd.read_csv(
        DATA_PATH
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df


def create_features(dates, price=29):

    df = pd.DataFrame({
        "date": dates
    })

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

    df["price_per_kg"] = price

    return df[
        [
            "day_of_year",
            "month",
            "day_of_week",
            "is_weekend",
            "price_per_kg"
        ]
    ]


def forecast_demand(days=7):

    model = load_model()

    history = load_history()

    last_date = history["date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=days,
        freq="D"
    )

    features = create_features(
        future_dates
    )

    predictions = model.predict(
        features
    )

    forecast = []

    for date, prediction in zip(
        future_dates,
        predictions
    ):

        forecast.append({
            "date": date.strftime(
                "%d %b"
            ),
            "demand_kg": int(
                max(0, prediction)
            )
        })

    return forecast