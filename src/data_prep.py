from pathlib import Path
import pandas as pd

SEASONS = ("winter", "spring", "summer", "autumn")
NEXT_SEASON = {"winter": "spring", "spring": "summer", "summer": "autumn", "autumn": "winter"}

SST_COLUMNS = {
    "oman": "oman_sst",
    "arab": "arabian_sea_sst",
    "sorkh": "red_sea_sst",
    "khalij fars": "persian_gulf_sst",
    "khazar": "caspian_sea_sst",
    "black sea": "black_sea_sst",
    "meditarane": "mediterranean_sst",
}


def load_clean_data(processed_dir: Path):
    sst = pd.read_csv(processed_dir / "sst_clean.csv")
    spi = pd.read_csv(processed_dir / "spi_clean_long.csv")
    regions = pd.read_csv(processed_dir / "regions.csv")
    return sst, spi, regions


def build_supervised_dataset(sst, spi, regions):
    years = sorted(sst["year"].unique())
    sst_idx = sst.set_index(["year", "season"])
    spi_idx = spi.set_index(["year", "season", "region_id"])["spi"]

    records = []
    for year in years:
        for season in SEASONS:
            next_season = NEXT_SEASON[season]
            target_year = year + 1 if season == "autumn" else year
            if target_year not in years:
                continue

            sst_row = sst_idx.loc[(year, season)]
            for region_id in regions["region_id"]:
                records.append({
                    "year": year,
                    "current_season": season,
                    "target_year": target_year,
                    "target_season": next_season,
                    "region_id": int(region_id),
                    "oman_sst": float(sst_row["oman_sst"]),
                    "arabian_sea_sst": float(sst_row["arabian_sea_sst"]),
                    "red_sea_sst": float(sst_row["red_sea_sst"]),
                    "persian_gulf_sst": float(sst_row["persian_gulf_sst"]),
                    "caspian_sea_sst": float(sst_row["caspian_sea_sst"]),
                    "black_sea_sst": float(sst_row["black_sea_sst"]),
                    "mediterranean_sst": float(sst_row["mediterranean_sst"]),
                    "spi_current": float(spi_idx.loc[(year, season, int(region_id))]),
                    "spi_next": float(spi_idx.loc[(target_year, next_season, int(region_id))]),
                })

    return pd.DataFrame(records).sort_values(
        ["region_id", "year", "current_season"]
    ).reset_index(drop=True)
