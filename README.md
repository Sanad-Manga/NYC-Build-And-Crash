# NYC-Build-And-Crash

Housing: DOB NOW Job Filings (https://data.cityofnewyork.us/d/w9ak-ipjd)

Transportation: Motor Vehicle Collisions (https://data.cityofnewyork.us/d/h9gi-nx95)

## Run the website

The site is a Streamlit app (Plotly charts). It currently runs on a **dummy** ZIP x year table (`data/dummy_zip_year.csv`, committed) and shows a "DUMMY DATA" banner. When the join notebook produces `data/zip_year.csv`, the app uses that file automatically and the banner disappears.

```bash
# from the repository root
python -m venv .venv
.venv\Scripts\activate            # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py              # opens http://localhost:8501
```

Use the sidebar filters (or type a search such as `Brooklyn 2022 new buildings` and press Enter), then click **Generate Report**: nothing on the page updates until you do.

Run the tests (search parser and data validation): `python -m pytest tests`

Regenerate the dummy data: `python scripts/make_dummy_data.py`

### Data contract for the real table

`data/zip_year.csv` (the join notebook's output) must follow this contract; `src/data.py::validate()` checks it and the app shows a clear error if it is broken.

| Column | Type | Rule |
|---|---|---|
| `zip_code` | string | exactly 5 digits, keep leading zeros (read with `dtype={"zip_code": str}`) |
| `year` | integer | 2022 to 2026 |
| `borough` | string | one of Manhattan, Brooklyn, Queens, Bronx, Staten Island (Title Case, no blanks) |
| `housing_job_count` | integer | unique jobs started in 2022 or later, counted from the initial I1 filings |
| `new_building_count` | integer | the same count, only for `job_type` New Building |
| `collision_count` | integer | crashes with a valid ZIP |
| `persons_injured`, `persons_killed`, `pedestrians_injured`, `cyclist_injured`, `motorist_injured` | integer | injured / killed counts |
| `is_partial_year` | boolean | True for 2026 (data ends 31 Oct) |

Rules:
- One row per `zip_code` x `year`. Duplicates are rejected.
- All counts are non-negative integers with **no NaN**.
- If a ZIP x year exists in only one source, the other source's counts are **0** and `borough` is taken from whichever source has it.
- Extra columns (for example `top_contributing_factor`) are allowed; the app ignores them.
