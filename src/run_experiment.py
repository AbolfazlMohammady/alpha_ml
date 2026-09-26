from pathlib import Path
import sys
import joblib
import pandas as pd

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import PROCESSED_DIR, OUTPUT_DIR
from src.data_prep import load_clean_data
from src.modeling import fit_region_model

def main():
    OUTPUT_DIR.joinpath("metrics").mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.joinpath("plots").mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.joinpath("models").mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(PROCESSED_DIR / "model_dataset.csv")
    all_metrics, all_predictions, all_importance = [], [], []

    for (region_id, season), group in data.groupby(["region_id", "current_season"], sort=True):
        model, metrics, predictions, importance = fit_region_model(group)
        metrics.update({"region_id": int(region_id), "current_season": season})
        importance["region_id"] = int(region_id)
        importance["current_season"] = season
        all_metrics.append(metrics)
        all_predictions.append(predictions)
        all_importance.append(importance)

        joblib.dump(
            model,
            OUTPUT_DIR / "models" / f"rf_region_{int(region_id):03d}_{season}.joblib"
        )

    pd.DataFrame(all_metrics).to_csv(OUTPUT_DIR / "metrics" / "model_metrics.csv", index=False)
    pd.concat(all_predictions, ignore_index=True).to_csv(
        OUTPUT_DIR / "metrics" / "predictions.csv", index=False
    )
    pd.concat(all_importance, ignore_index=True).to_csv(
        OUTPUT_DIR / "metrics" / "feature_importance.csv", index=False
    )

if __name__ == "__main__":
    main()
