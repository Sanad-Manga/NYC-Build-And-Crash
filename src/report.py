"""Filtering and summary numbers behind the "Generate Report" button (no Streamlit code here)."""
import pandas as pd

# metric column -> (dropdown label, axis unit). Order = order in the metric dropdown.
METRICS = {
    "housing_job_count": ("Housing jobs started", "jobs"),
    "new_building_count": ("New-building jobs started", "jobs"),
    "collision_count": ("Collisions", "crashes"),
    "persons_injured": ("Persons injured", "people"),
    "persons_killed": ("Persons killed", "people"),
    "pedestrians_injured": ("Pedestrians injured", "people"),
    "cyclist_injured": ("Cyclists injured", "people"),
    "motorist_injured": ("Motorists injured", "people"),
}


def metric_label(metric: str) -> str:
    """Human-readable name of a metric column."""
    return METRICS[metric][0]


def axis_title(metric: str) -> str:
    """Axis title with units, e.g. 'Collisions (crashes)'."""
    label, unit = METRICS[metric]
    return f"{label} ({unit})"


def apply_filters(df: pd.DataFrame, borough=None, year=None, zips=None) -> pd.DataFrame:
    """Keep the rows matching every filter that is set (None / empty list = no filter)."""
    out = df
    if borough:
        out = out[out["borough"] == borough]
    if year:
        out = out[out["year"] == year]
    if zips:
        out = out[out["zip_code"].isin(zips)]
    return out


def filters_text(borough=None, year=None, zips=None) -> str:
    """Short description of the active filters, used in chart titles and the summary."""
    parts = [borough or "All boroughs", str(year) if year else "2022-2026"]
    if zips:
        parts.append(f"{len(zips)} ZIP(s) selected")
    return ", ".join(parts)


def summary(df: pd.DataFrame, metric: str) -> dict:
    """Headline numbers for the filtered table (the metric is summed over all matching rows)."""
    by_zip = df.groupby("zip_code")[metric].sum()
    top_zip = by_zip.idxmax() if len(by_zip) else None
    return {
        "total": int(df[metric].sum()),
        "zip_count": int(df["zip_code"].nunique()),
        "top_zip": top_zip,
        "top_zip_value": int(by_zip.max()) if top_zip else 0,
        "includes_partial_year": bool(df["is_partial_year"].any()),
    }
