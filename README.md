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

Run the tests (search parser): `python -m pytest tests`

Regenerate the dummy data: `python scripts/make_dummy_data.py`
