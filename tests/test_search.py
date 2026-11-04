"""Tests for src/search.py::parse_query. Run from the repo root: python -m pytest tests"""
import pytest

from src.search import describe_query, parse_query


def parsed(**overrides):
    """Expected result with every field empty, then overridden."""
    base = {"borough": None, "year": None, "metric": None, "zip_code": None, "unparsed": []}
    base.update(overrides)
    return base


def test_example_from_the_brief():
    assert parse_query("Brooklyn 2022 new buildings") == parsed(
        borough="Brooklyn", year=2022, metric="new_building_count")


def test_zip_code_and_year():
    assert parse_query("10001 2024 collisions") == parsed(
        zip_code="10001", year=2024, metric="collision_count")


def test_leading_zero_zip_stays_a_string():
    assert parse_query("07001")["zip_code"] == "07001"


def test_typo_is_returned_as_unparsed_not_guessed():
    result = parse_query("Brooklin 2022 crashes")
    assert result["borough"] is None
    assert result["unparsed"] == ["brooklin"]
    assert (result["year"], result["metric"]) == (2022, "collision_count")


def test_empty_blank_and_none_input():
    assert parse_query("") == parsed()
    assert parse_query("   ") == parsed()
    assert parse_query(None) == parsed()


def test_case_insensitive_and_the_prefix():
    assert parse_query("THE BRONX 2023 injuries") == parsed(
        borough="Bronx", year=2023, metric="persons_injured")


def test_borough_abbreviations():
    assert parse_query("bk")["borough"] == "Brooklyn"
    assert parse_query("SI housing")["borough"] == "Staten Island"


def test_staten_island_two_words():
    assert parse_query("Staten Island new construction 2025") == parsed(
        borough="Staten Island", year=2025, metric="new_building_count")


def test_nyc_means_no_borough_filter_and_is_not_unparsed():
    assert parse_query("nyc crashes") == parsed(metric="collision_count")


def test_new_buildings_is_not_read_as_plain_buildings():
    assert parse_query("new buildings")["metric"] == "new_building_count"
    assert parse_query("buildings")["metric"] == "housing_job_count"
    assert parse_query("filings jobs housing")["metric"] == "housing_job_count"


def test_year_outside_range_is_ignored():
    result = parse_query("Queens 2019")
    assert result["year"] is None
    assert result["unparsed"] == ["2019"]
    assert result["borough"] == "Queens"


def test_unknown_words_are_listed():
    result = parse_query("Queens 2022 pizza")
    assert result["unparsed"] == ["pizza"]
    assert result["borough"] == "Queens"


def test_punctuation_is_ignored():
    assert parse_query("Brooklyn, 2022! new buildings.") == parsed(
        borough="Brooklyn", year=2022, metric="new_building_count")


def test_second_borough_goes_to_unparsed():
    result = parse_query("Brooklyn Queens")
    assert result["borough"] == "Brooklyn"
    assert result["unparsed"] == ["queens"]


def test_describe_query_text():
    understood, ignored = describe_query(parse_query("Brooklyn 2022 pizza"))
    assert "borough = Brooklyn" in understood and "year = 2022" in understood
    assert ignored == "pizza"
    assert describe_query(parse_query(""))[0] == "nothing recognised"
