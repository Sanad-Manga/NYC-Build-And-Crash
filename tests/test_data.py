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
