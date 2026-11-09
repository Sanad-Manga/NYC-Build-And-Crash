# NYC Build and Crash

Course project (Data Engineering and Visualization, Milestone 1). We ask whether the NYC neighborhoods (ZIP codes) with the most new construction also have more traffic collisions, and show the answer in an interactive website. We only describe association between the two datasets, never cause and effect.

## Datasets

| Domain | Dataset | Link |
|---|---|---|
| Housing and Development | DOB NOW: Build - Job Application Filings (`w9ak-ipjd`) | https://data.cityofnewyork.us/d/w9ak-ipjd |
| Transportation | Motor Vehicle Collisions - Crashes (`h9gi-nx95`) | https://data.cityofnewyork.us/d/h9gi-nx95 |

The two datasets share no row-level key, so both are aggregated to **ZIP code x year** and the summaries are combined (no row-level join). Scope is 2022-01-01 onward; 2026 is a partial year (data ends 31 Oct).

## Repository layout

```
app.py                                     Streamlit website (thin: layout only)
src/                                       website logic: data.py (load + validate), search.py, report.py, charts.py
scripts/make_dummy_data.py                 generates data/dummy_zip_year.csv
data/dummy_zip_year.csv                    committed fake ZIP x year table used until the real one exists
phase1_housing_initial_cleaning_issa.ipynb housing: loading and cleaning
phase1_collisions_eda_cleaning_ahmed.ipynb collisions: feasibility check, EDA and cleaning
tests/                                     pytest tests (search parser, data validation)
AI_PROMPTS.txt                             log of the AI prompts used, per member
requirements.txt                           one shared, pinned dependency file
```

`data/` is git-ignored except the dummy table: notebooks download their own data from the API or read the previous notebook's output.

## Setup (VS Code + Python venv)

No Colab, no Google Drive: everything runs locally with relative paths. Tested with Python 3.14 on Windows.

```bash
# from the repository root
python -m venv .venv
.venv\Scripts\activate            # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

In VS Code install the **Python** and **Jupyter** extensions, open the folder, and choose the `.venv` interpreter (bottom right, or Ctrl+Shift+P, "Python: Select Interpreter").

All members add their packages to the single `requirements.txt` (pinned versions); do not create a second requirements file.

## Run the notebooks

Open a notebook in VS Code, click **Select Kernel** and pick `.venv`, then **Restart** and **Run All**.

- `phase1_collisions_eda_cleaning_ahmed.ipynb`: the first run downloads about 450k collision rows from the NYC Open Data API (1-2 minutes) into `data/collisions_raw.csv`; later runs reuse that file. It ends by writing `data/collisions_step2.csv.gz`.
- `phase1_housing_initial_cleaning_issa.ipynb`: housing loading and cleaning. Its fixes are still under review in an open pull request.

The collisions notebook ends with a "Prompts used" cell that points to `AI_PROMPTS.txt`; the course requires one in every notebook.

## Run the website

The site is a Streamlit app (Plotly charts). It currently runs on a **dummy** ZIP x year table (`data/dummy_zip_year.csv`, committed) and shows a "DUMMY DATA" banner. When the join notebook produces `data/zip_year.csv`, the app uses that file automatically and the banner disappears.

```bash
# from the repository root, with the venv active
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

## Deployment (Render)

*Owner: Mohamed Walid. To be filled in once the deployment works; nothing below has been run yet.*

- Live URL: _to be added_
- Build command: _to be added_
- Start command: _to be added_
- Python version and environment variables: _to be added_
- Data: `data/zip_year.csv` is git-ignored, so the deployment must either commit it or generate it during the build. Decision: _to be added_

## Website on Vercel (Dash)

`dash_app.py` is the Dash version of the website (same `src/` logic, same Plotly charts); `app.py` (Streamlit) stays as a fallback. Vercel cannot run Streamlit (it needs a long-running server), so the deployed site is the Dash app.

```bash
# from the repository root, with the venv active (pip install -r requirements.txt; it includes dash)
python dash_app.py                # opens http://127.0.0.1:8050
```

Tabs: **Dashboard** (search box, Borough / Year / Housing category / Collision category / optional ZIP dropdowns, **Generate Report**; nothing updates until the button is clicked), **Research questions** (reads `assets/rq/<name>_q<1|2>.md` and `.png`; missing files show "not yet available") and **Story**. If `data/zip_year.csv` is missing the site falls back to `data/dummy_zip_year.csv` and shows a "Showing dummy data" banner. The housing categories "Alterations" and "Demolitions" are hidden (with a note) when `alteration_job_count` / `demolition_job_count` are absent from the table.

### Vercel packaging (exception to the one-requirements.txt rule)

The root `requirements.txt` stays the single file for the notebooks, tests and the Streamlit fallback. The Vercel function must not install notebook packages (jupyter, seaborn, nbconvert, pytest ...), so the **web dependencies live in `pyproject.toml`** (`dash==4.4.1`, `plotly==7.1.0`, `pandas==3.1.0`, `numpy==2.5.4`; the last three match `requirements.txt`). `[tool.vercel] entrypoint = "vercel_app:app"` points Vercel at `vercel_app.py`, which exposes the Flask object of the Dash app as `app`. `.python-version` selects Python 3.14, and `vercel.json` excludes notebooks, tests and docs from the function bundle. The data file and `assets/` are bundled because Vercel includes every file reachable in the project. The lean dependency set measured 294 MB of installed packages in a fresh virtual environment (limit: 500 MB uncompressed per the Vercel docs).

Vercel project settings (set once in the Vercel dashboard, after signing in with GitHub):

1. New Project, import `Sanad-Manga/NYC-Build-And-Crash`.
2. Framework Preset: **Other**.
3. Root Directory: leave empty (repository root).
4. Build Command, Output Directory: leave empty (no override). Install Command: leave empty (Vercel installs from `pyproject.toml`).
5. Environment Variables: none.
6. Production Branch: **main** (Settings, Git).
7. Deploy. Python version comes from `.python-version` (3.14); no setting needed.
8. In the build log check that jupyter / streamlit / seaborn are NOT being installed. If they are, tell the team: the install command has to be overridden.

*Status: tested locally (tests, WSGI test client, browser click-through). The live deployment is to be confirmed by Ahmed after the first Vercel build.*

## Team and contributions

Team of four. Status reflects the repository on 5 Nov 2026; "open PR" means the work is in a pull request that is not merged yet.

| Member | Work | Status |
|---|---|---|
| **Ahmed Sanad** (team leader) | Collisions feasibility check, EDA and cleaning notebook (ZIP, coordinates, outliers, export) | merged |
| | Website skeleton: sidebar filters, search mode, Generate Report button, four charts, story section, data validation and tests, dummy data | merged |
| | Prompt log file and entry format; this README | merged / this PR |
| **Mohamed Issa** | Housing data loading and cleaning notebook | on main; fixes in open PR |
| | ZIP x year join of the two datasets | planned, not in the repository yet |
| **Mohamed Walid** | Housing EDA, outliers, cleaning and validation | open PR |
| | Render deployment | in progress |
| | Proposed team standards | open PR |
| **Yassin** | Collisions loading and cleaning (stage 1) | open PR |
| | Map visualization and final notebook assembly | planned |

### Research questions and visualizations

Each member writes 2 research questions and builds 2 visualizations (8 of each in total). *To be filled in by each member with their own questions, chart type and file/location.*

| Member | Question 1 / Visualization 1 | Question 2 / Visualization 2 |
|---|---|---|
| Ahmed Sanad | _to be added_ | _to be added_ |
| Mohamed Issa | _to be added_ | _to be added_ |
| Mohamed Walid | _to be added_ | _to be added_ |
| Yassin | _to be added_ | _to be added_ |

### Use of AI

Every member logs the AI prompts that shaped their work in `AI_PROMPTS.txt` (date, student, tool, requirement, prompt, how the output was used).

## Limitations

- About 28% of collisions have no ZIP code, so ZIP-level collision counts are undercounts, more so in 2022-2023.
- 2026 is a partial year (data ends 31 Oct); never compare its totals with full years.
- There is no traffic-volume data: a busy ZIP may simply have more cars and people.
- Counts are not normalised by area or population.
- Everything here is association between two datasets, not evidence that one causes the other.
