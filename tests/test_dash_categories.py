"""Tests for the Dash site's category handling: optional columns, category search, research scanner."""
import pandas as pd
import pytest

from src.data import DUMMY_PATH, REQUIRED_COLUMNS, DataValidationError, validate
from src.report import COLLISION_CATEGORIES, HOUSING_CATEGORIES, available_categories, axis_title, metric_label
from src.research import NOT_AVAILABLE, scan_research
from src.search import describe_categories, parse_categories


@pytest.fixture
def table() -> pd.DataFrame:
    return pd.read_csv(DUMMY_PATH, dtype={"zip_code": str}).head(10)


# ---- optional columns
def test_optional_columns_are_kept_when_present(table):
    table["alteration_job_count"] = 5
    table["demolition_job_count"] = 1
    result = validate(table)
    assert list(result.columns) == REQUIRED_COLUMNS + ["alteration_job_count", "demolition_job_count"]


def test_absent_optional_columns_hide_their_categories(table):
    result = validate(table)
    housing = available_categories(HOUSING_CATEGORIES, result.columns)
    assert list(housing) == ["All jobs", "New buildings"]
    assert len(available_categories(COLLISION_CATEGORIES, result.columns)) == 6


def test_bad_optional_column_raises(table):
    table["demolition_job_count"] = -1
    with pytest.raises(DataValidationError, match="demolition_job_count"):
        validate(table)


def test_labels_cover_optional_metrics():
    assert metric_label("alteration_job_count") == "Alteration jobs started"
    assert axis_title("demolition_job_count").endswith("(jobs)")


# ---- category search
def test_example_with_two_categories():
    parsed = parse_categories("Queens 2024 demolitions cyclists")
    assert (parsed["borough"], parsed["year"]) == ("Queens", 2024)
    assert (parsed["housing"], parsed["collision"]) == ("demolition_job_count", "cyclist_injured")
    assert parsed["unparsed"] == []


def test_brief_example_new_buildings():
    parsed = parse_categories("Brooklyn 2022 new buildings")
    assert (parsed["borough"], parsed["year"], parsed["housing"]) == ("Brooklyn", 2022, "new_building_count")
    assert parsed["collision"] is None


@pytest.mark.parametrize("text,column", [
    ("persons killed", "persons_killed"), ("pedestrians injured", "pedestrians_injured"),
    ("motorists", "motorist_injured"), ("injuries", "persons_injured"), ("crashes", "collision_count")])
def test_collision_phrases(text, column):
    assert parse_categories(text)["collision"] == column


def test_alterations_and_zip():
    parsed = parse_categories("10001 alterations")
    assert (parsed["zip_code"], parsed["housing"]) == ("10001", "alteration_job_count")


def test_nonsense_never_raises_and_is_reported():
    parsed = parse_categories("asdf qwerty ???")
    assert parsed["unparsed"] == ["asdf", "qwerty"]
    assert describe_categories(parsed)[0] == "nothing recognised"
    assert parse_categories(None)["unparsed"] == [] and parse_categories("")["housing"] is None


def test_second_phrase_for_same_category_is_ignored():
    parsed = parse_categories("demolitions alterations")
    assert parsed["housing"] == "alteration_job_count" or parsed["housing"] == "demolition_job_count"
    assert len(parsed["unparsed"]) == 1


# ---- research-question scanner
def test_empty_folder_gives_eight_unavailable_entries(tmp_path):
    entries = scan_research(tmp_path)
    assert len(entries) == 8
    assert not any(e["available"] for e in entries)
    assert all(e["question"] == NOT_AVAILABLE and e["image"] is None for e in entries)


def test_missing_folder_does_not_crash(tmp_path):
    assert len(scan_research(tmp_path / "nope")) == 8


def test_normal_case_reads_question_finding_and_image(tmp_path):
    (tmp_path / "ahmed_q1.md").write_text("Is X related to Y?\nA weak positive association.\nSecond line.\n",
                                          encoding="utf-8")
    (tmp_path / "ahmed_q1.png").write_bytes(b"png")
    entry = scan_research(tmp_path)[0]
    assert entry["available"] and entry["name"] == "ahmed" and entry["number"] == 1
    assert entry["question"] == "Is X related to Y?"
    assert entry["finding"] == "A weak positive association.\nSecond line."
    assert entry["image"] == "ahmed_q1.png"


def test_missing_png_keeps_text(tmp_path):
    (tmp_path / "issa_q2.md").write_text("Question?\nFinding.", encoding="utf-8")
    entry = next(e for e in scan_research(tmp_path) if e["name"] == "issa" and e["number"] == 2)
    assert entry["available"] and entry["image"] is None


def test_png_without_md_is_unavailable(tmp_path):
    (tmp_path / "walid_q1.png").write_bytes(b"x")
    entry = next(e for e in scan_research(tmp_path) if e["name"] == "walid" and e["number"] == 1)
    assert not entry["available"] and entry["finding"] == NOT_AVAILABLE


def test_empty_md_file_is_unavailable(tmp_path):
    (tmp_path / "yassin_q1.md").write_text("", encoding="utf-8")
    assert not next(e for e in scan_research(tmp_path) if e["name"] == "yassin")["available"]
