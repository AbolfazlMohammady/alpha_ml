from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_DIR = ROOT_DIR / "outputs"

FEATURE_COLUMNS = [
    "oman_sst",
    "arabian_sea_sst",
    "red_sea_sst",
    "persian_gulf_sst",
    "caspian_sea_sst",
    "black_sea_sst",
    "mediterranean_sst",
    "spi_current",
]
TARGET_COLUMN = "spi_next"
SEASONS = ("winter", "spring", "summer", "autumn")
RANDOM_STATE = 42
TEST_FRACTION = 0.20
N_ESTIMATORS = 200
