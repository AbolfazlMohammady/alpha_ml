# ALPHA ML — SPI Forecasting with Random Forest Regression

## Project goal
Predict next-season SPI for each of 154 regions using:
- 7 current-season sea-surface-temperature (SST) features
- current-season SPI for the same region

The project specification requests Random Forest Regression, train/test evaluation with R², RMSE and MAE, and feature-importance analysis.

## Data
Source period: 1891–2023 (133 years).

- SST: 4 seasons × 7 sea regions.
- SPI: 4 seasons × 154 spatial regions.
- No missing values were found in the source observations used here.

## Important temporal rule
The seasonal sequence is:

winter → spring → summer → autumn → next winter.

Therefore, `autumn 2022 → winter 2023` is valid, while `autumn 2023 → winter 2024` is not available and is excluded. This avoids manufacturing a target that does not exist in the supplied data.

## Folder structure

```text
alpha_ml/
├── data/
│   ├── raw/                  # Original supplied files
│   └── processed/            # Clean, analysis-ready data
├── notebooks/
│   ├── 01_data_validation.ipynb
│   ├── 02_prepare_dataset.ipynb
│   ├── 03_train_random_forest.ipynb
│   └── 04_evaluate_and_feature_importance.ipynb
├── src/
│   ├── config.py
│   ├── data_prep.py
│   ├── modeling.py
│   └── run_experiment.py
├── outputs/
│   ├── metrics/
│   ├── models/
│   └── plots/
├── reports/
├── requirements.txt
└── README.md
```

## Run
```bash
python -m pip install -r requirements.txt
jupyter notebook
```

Recommended notebook order:
1. `01_data_validation.ipynb`
2. `02_prepare_dataset.ipynb`
3. `03_train_random_forest.ipynb`
4. `04_evaluate_and_feature_importance.ipynb`

The training split is chronological rather than shuffled to reduce temporal leakage in this time-series problem.
