"""Tests for src/data.py (schema validation). Run from the repo root: python -m pytest tests"""
import pandas as pd
import pytest

from src.data import DUMMY_PATH, REQUIRED_COLUMNS, DataValidationError, load_data, validate


@pytest.fixture
def table() -> pd.DataFrame:
    """A small valid table: the first rows of the committed dummy file (zip_code read as a string)."""
    return pd.read_csv(DUMMY_PATH, dtype={"zip_code": str}).head(10)


def test_valid_table_passes(table):
    result = validate(table)
    assert list(result.columns) == REQUIRED_COLUMNS
    assert len(result) == len(table)


def test_extra_column_is_allowed_and_dropped(table):
    table["top_contributing_factor"] = "Driver Inattention/Distraction"
    result = validate(table)
    assert "top_contributing_factor" not in result.columns
    assert list(result.columns) == REQUIRED_COLUMNS


def test_extra_column_in_a_csv_file_loads(table, tmp_path):
    path = tmp_path / "zip_year.csv"
    table.assign(pedestrians_killed=0).to_csv(path, index=False)
    assert list(load_data(path).columns) == REQUIRED_COLUMNS


def test_missing_required_column_raises(table):
    with pytest.raises(DataValidationError, match="collision_count"):
        validate(table.drop(columns=["collision_count"]))


def test_zip_that_is_not_five_digits_raises(table):
    table.loc[table.index[0], "zip_code"] = "1001"
    with pytest.raises(DataValidationError, match="zip_code"):
        validate(table)


def test_duplicate_zip_year_raises(table):
    duplicated = pd.concat([table, table.head(1)], ignore_index=True)
    with pytest.raises(DataValidationError, match="duplicates"):
        validate(duplicated)


def test_blank_borough_raises(table):
    table.loc[table.index[0], "borough"] = None
    with pytest.raises(DataValidationError, match="borough"):
        validate(table)


def test_negative_count_raises(table):
    table.loc[table.index[0], "collision_count"] = -1
    with pytest.raises(DataValidationError, match="negative"):
        validate(table)


def test_real_file_shape_loads(table, tmp_path):
    """The integration notebook's real output has extra columns (flag, top factor, match status), leading-zero
    ZIPs and a partial 2026: the loader must keep the required columns and the 5-digit string ZIPs."""
    real = table.copy()
    real.loc[real.index[0], "zip_code"] = "00083"
    real.loc[real.index[1], "zip_code"] = "10999"
    real.loc[real.index[1], "year"] = 2026
    real.loc[real.index[1], "is_partial_year"] = True
    real["low_data_flag"] = False
    real.loc[real.index[2], "low_data_flag"] = True
    real["top_contributing_factor"] = "Driver Inattention/Distraction"
    real["match_status"] = "both"
    path = tmp_path / "zip_year.csv"
    real.to_csv(path, index=False)
    result = load_data(path)
    assert list(result.columns) == REQUIRED_COLUMNS
    assert result["zip_code"].str.fullmatch(r"\d{5}").all() and "00083" in set(result["zip_code"])
    assert result["is_partial_year"].dtype == bool and (result.loc[result["year"] == 2026, "is_partial_year"]).all()


def test_committed_real_table_validates_when_present():
    """If data/zip_year.csv exists on this machine, it must pass the website validator (skipped otherwise)."""
    from src.data import REAL_PATH
    if not REAL_PATH.exists():
        pytest.skip("data/zip_year.csv not present (it is git-ignored until deployment)")
    assert len(load_data(REAL_PATH)) > 0
