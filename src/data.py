"""Load and validate the ZIP x year table that feeds the website.

To switch from the dummy table to the real one, put the join notebook's output at
data/zip_year.csv. `resolve_data_path()` then picks it automatically; nothing else changes.

Extra columns in the file (e.g. top_contributing_factor, pedestrians_killed) are allowed:
they are ignored and dropped after validation. Only a missing REQUIRED column is an error.
"""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REAL_PATH = DATA_DIR / "zip_year.csv"            # produced by the join notebook (git-ignored)
DUMMY_PATH = DATA_DIR / "dummy_zip_year.csv"     # committed fake table, see scripts/make_dummy_data.py

BOROUGHS = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
YEAR_MIN, YEAR_MAX = 2022, 2026

COUNT_COLUMNS = [
    "housing_job_count", "new_building_count", "collision_count", "persons_injured",
    "persons_killed", "pedestrians_injured", "cyclist_injured", "motorist_injured",
]
REQUIRED_COLUMNS = ["zip_code", "year", "borough"] + COUNT_COLUMNS + ["is_partial_year"]


class DataValidationError(ValueError):
    """Raised when the ZIP x year table does not follow the agreed schema."""


def resolve_data_path() -> Path:
    """Return the real table if it exists, otherwise the dummy one (single switch point)."""
    return REAL_PATH if REAL_PATH.exists() else DUMMY_PATH


def is_dummy(path) -> bool:
    """True when `path` is the fake table, so the app can show its DUMMY DATA banner."""
    return Path(path).name == DUMMY_PATH.name


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Check columns, dtypes and value ranges; raise DataValidationError with a clear message.

    Extra columns are allowed. On success only the REQUIRED_COLUMNS are returned (a copy).
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise DataValidationError(f"Required columns are missing: {missing}")

    if not df["zip_code"].map(lambda z: isinstance(z, str) and len(z) == 5 and z.isdigit()).all():
        raise DataValidationError("zip_code must be a 5-digit string (e.g. '10001'); found other values.")
    if not pd.api.types.is_integer_dtype(df["year"]):
        raise DataValidationError(f"year must be an integer column, got {df['year'].dtype}.")
    if not df["year"].between(YEAR_MIN, YEAR_MAX).all():
        raise DataValidationError(f"year must be between {YEAR_MIN} and {YEAR_MAX}.")
    bad_boroughs = sorted(set(df["borough"].dropna()) - set(BOROUGHS))
    if bad_boroughs or df["borough"].isna().any():
        raise DataValidationError(
            f"borough must be one of {BOROUGHS} (Title Case, no blanks); found {bad_boroughs}.")
    for col in COUNT_COLUMNS:
        if not pd.api.types.is_integer_dtype(df[col]):
            raise DataValidationError(f"{col} must be an integer count column, got {df[col].dtype}.")
        if (df[col] < 0).any():
            raise DataValidationError(f"{col} contains negative counts.")
    if df["is_partial_year"].dtype != bool:
        raise DataValidationError("is_partial_year must be a boolean column.")
    if df.duplicated(["zip_code", "year"]).any():
        raise DataValidationError("There must be exactly one row per zip_code x year; found duplicates.")
    return df[REQUIRED_COLUMNS].copy()


def load_data(path=None) -> pd.DataFrame:
    """Read the ZIP x year CSV (zip_code as a string so leading zeros survive) and validate it."""
    path = Path(path) if path is not None else resolve_data_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}. Run scripts/make_dummy_data.py or add data/zip_year.csv.")
    df = pd.read_csv(path, dtype={"zip_code": str})
    return validate(df)
