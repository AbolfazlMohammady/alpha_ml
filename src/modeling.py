import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .config import FEATURE_COLUMNS, TARGET_COLUMN, RANDOM_STATE, N_ESTIMATORS


def chronological_split(df, test_fraction=0.20):
    df = df.sort_values("year").reset_index(drop=True)
    n_test = max(1, int(np.ceil(len(df) * test_fraction)))
    split = len(df) - n_test
    return df.iloc[:split].copy(), df.iloc[split:].copy()


def fit_region_model(region_df, test_fraction=0.20):
    train, test = chronological_split(region_df, test_fraction)
    model = RandomForestRegressor(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        max_features=1.0,
    )
    model.fit(train[FEATURE_COLUMNS], train[TARGET_COLUMN])
    prediction = model.predict(test[FEATURE_COLUMNS])

    metrics = {
        "train_year_start": int(train["year"].min()),
        "train_year_end": int(train["year"].max()),
        "test_year_start": int(test["year"].min()),
        "test_year_end": int(test["year"].max()),
        "n_train": len(train),
        "n_test": len(test),
        "r2": float(r2_score(test[TARGET_COLUMN], prediction)),
        "rmse": float(np.sqrt(mean_squared_error(test[TARGET_COLUMN], prediction))),
        "mae": float(mean_absolute_error(test[TARGET_COLUMN], prediction)),
    }
    predictions = test[["year", "current_season", "target_year", "target_season", "region_id"]].copy()
    predictions["actual_spi"] = test[TARGET_COLUMN].to_numpy()
    predictions["predicted_spi"] = prediction
    feature_importance = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    return model, metrics, predictions, feature_importance
