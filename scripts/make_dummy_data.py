"""Generate data/dummy_zip_year.csv: a clearly FAKE ZIP x year table for building the website.

The numbers are random (seeded, so the file is reproducible) and say nothing about the real
city. The real table (data/zip_year.csv) comes from the join notebook and replaces this file.

Run from the repository root:  python scripts/make_dummy_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
YEARS = [2022, 2023, 2024, 2025, 2026]
PARTIAL_YEAR = 2026            # data ends 31 Oct, so only 10 of 12 months
PARTIAL_SHARE = 10 / 12
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "dummy_zip_year.csv"

# 60 real NYC ZIP codes (5-digit strings) grouped by borough; only the numbers below are fake.
ZIPS_BY_BOROUGH = {
    "Manhattan": ["10001", "10002", "10003", "10009", "10011", "10016", "10019", "10025",
                  "10027", "10029", "10031", "10033", "10036", "10128"],
    "Brooklyn": ["11201", "11205", "11206", "11207", "11211", "11215", "11216", "11220",
                 "11222", "11225", "11226", "11230", "11233", "11234", "11235", "11237"],
    "Queens": ["11101", "11354", "11355", "11368", "11373", "11375", "11377", "11385",
               "11411", "11412", "11421", "11432", "11434", "11691"],
    "Bronx": ["10451", "10452", "10455", "10456", "10457", "10458", "10460", "10462",
              "10466", "10468"],
    "Staten Island": ["10301", "10304", "10305", "10306", "10309", "10312"],
}

# Rough per-borough activity levels (fake) so the charts show some spread between boroughs.
BOROUGH_TRAFFIC = {"Manhattan": 1.2, "Brooklyn": 1.3, "Queens": 1.0, "Bronx": 1.1, "Staten Island": 0.5}
BOROUGH_BUILDING = {"Manhattan": 1.0, "Brooklyn": 1.4, "Queens": 1.2, "Bronx": 0.9, "Staten Island": 0.5}


def make_dummy_table(seed: int = SEED) -> pd.DataFrame:
    """Return the fake ZIP x year table with the agreed column names."""
    rng = np.random.default_rng(seed)
    rows = []
    for borough, zips in ZIPS_BY_BOROUGH.items():
        for zip_code in zips:
            busy = rng.lognormal(0.0, 0.45) * BOROUGH_TRAFFIC[borough]
            # construction level is only loosely tied to how busy a ZIP is
            dev = rng.lognormal(0.0, 0.6) * BOROUGH_BUILDING[borough] * busy ** 0.3
            for year in YEARS:
                share = PARTIAL_SHARE if year == PARTIAL_YEAR else 1.0
                trend_c = 1 - 0.05 * (year - 2022)       # fake: collisions drift down a little
                trend_h = 1 + 0.04 * (year - 2022)       # fake: filings drift up a little
                collisions = rng.poisson(300 * busy * trend_c * share)
                housing = rng.poisson(450 * dev * trend_h * share)
                new_buildings = rng.poisson(housing * rng.uniform(0.04, 0.09))
                ped = rng.poisson(collisions * 0.10)
                cyc = rng.poisson(collisions * 0.055)
                mot = rng.poisson(collisions * 0.38)
                rows.append({
                    "zip_code": zip_code,
                    "year": year,
                    "borough": borough,
                    "housing_job_count": housing,
                    "new_building_count": new_buildings,
                    "collision_count": collisions,
                    "persons_injured": ped + cyc + mot,      # total = sum of the three parts
                    "persons_killed": rng.poisson(collisions * 0.0028),
                    "pedestrians_injured": ped,
                    "cyclist_injured": cyc,
                    "motorist_injured": mot,
                    "is_partial_year": year == PARTIAL_YEAR,
                })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = make_dummy_table()
    OUT_PATH.parent.mkdir(exist_ok=True)
    table.to_csv(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH.name}: {len(table)} rows, {table['zip_code'].nunique()} ZIPs")
