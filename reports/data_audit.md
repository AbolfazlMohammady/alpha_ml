# Data Audit Report

## Source files

- `data/raw/project_specification.pdf`
- `data/raw/sst_source.xlsx`
- `data/raw/spi_source.xlsx`

## Verified structure

### SST
- 4 seasons: winter, spring, summer, autumn
- 133 observations per season
- years assigned from 1891 through 2023 based on the 133-row source sequence
- 7 SST variables
- 0 missing numeric values
- 0 duplicate years within a season

### SPI
- 4 seasons
- 133 years: 1891–2023
- 154 spatial regions
- 0 missing SPI values
- 0 duplicate years within a season
- 154 unique `(lon, lat)` region locations

## Supervised dataset

- Rows: 81,774
- Columns: 14
- Regions: 154
- Missing values: 0
- Duplicate `(year, current_season, region_id)` keys: 0

### Features

1. `oman_sst`
2. `arabian_sea_sst`
3. `red_sea_sst`
4. `persian_gulf_sst`
5. `caspian_sea_sst`
6. `black_sea_sst`
7. `mediterranean_sst`
8. `spi_current`

Target: `spi_next`

## Temporal handling

The sequence is:

`winter → spring → summer → autumn → next winter`

Therefore `autumn 2023 → winter 2024` is excluded because winter 2024 is not present in the supplied files. No synthetic target was created.

## Cleaning decisions

Only structural noise was removed:
- extra/blank header rows in the Excel files
- duplicate-looking Excel-generated column labels were not used as region identifiers
- stable region IDs and coordinates were created from the supplied longitude/latitude rows
- SST column names were normalized to English `snake_case`

No numeric values were imputed, clipped, standardized, or otherwise altered.
