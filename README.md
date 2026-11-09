# NYC Build and Crash

Team project for **Data Engineering and Visualization** (German International University, Milestone 1, due 9 Nov 2026).

**Question.** Do the NYC neighborhoods (ZIP codes) with the most new construction also have more, or different, traffic collisions? We answer it with two NYC Open Data datasets, a documented cleaning and integration pipeline, eight research questions, and an interactive website. We only describe association between the two datasets, never cause and effect.

- **Live website:** https://nyc-build-and-crash.vercel.app (to be confirmed by Ahmed as the URL submitted)
- **Repository:** https://github.com/Sanad-Manga/NYC-Build-And-Crash

## Datasets

| Domain | Dataset | ID | Link |
|---|---|---|---|
| Housing and Development | DOB NOW: Build - Job Application Filings | `w9ak-ipjd` | https://data.cityofnewyork.us/d/w9ak-ipjd |
| Transportation | Motor Vehicle Collisions - Crashes | `h9gi-nx95` | https://data.cityofnewyork.us/d/h9gi-nx95 |

The two datasets share no row-level key, so each is aggregated to **ZIP code x year** and the two summaries are joined (outer join); individual filings are never matched to individual crashes. Scope is 2022-01-01 onward; 2026 is a partial year (January to October).

## Repository layout

```
00_project_overview.ipynb                    overview of data, pipeline, run order and the eight findings (Yassin)
phase1_housing_initial_cleaning_issa.ipynb   housing: loading, missing values, duplicates
phase1_housing_eda_cleaning_walid.ipynb      housing: EDA, outliers, inconsistencies, ZIP/date standards
phase1_collisions_initial_cleaning_yassin.ipynb  collisions: initial cleaning and audit
phase1_collisions_eda_cleaning_ahmed.ipynb   collisions: EDA, ZIP/coordinate cleaning, export
phase2_housing_zip_year_walid.ipynb          housing aggregated to ZIP x year
phase2_collisions_aggregation_yassin.ipynb   collisions aggregated to ZIP x year
phase2_data_integration_issa.ipynb           join, post-join cleaning, writes data/zip_year.csv
phase3_analysis_ahmed.ipynb                  research questions (Ahmed)
phase3_analysis_issa.ipynb                   research questions (Issa)
phase3_analysis_walid.ipynb                  research questions (Walid)
phase3_analysis_yassin.ipynb                 research questions (Yassin)
dash_app.py                                  the website (Dash)
vercel_app.py, vercel.json, pyproject.toml   Vercel entry point and web-only dependencies
app.py                                       earlier Streamlit version of the website (kept as a fallback)
src/                                         website logic: data.py, search.py, report.py, charts.py, research.py
assets/rq/                                   the 8 research-question charts (.png) and findings (.md)
assets/style.css                             website styling
data/zip_year.csv                            the integrated ZIP x year table (committed)
data/dummy_zip_year.csv                      fake table used only if zip_year.csv is missing
scripts/make_dummy_data.py                   generates the dummy table
tests/                                       pytest tests (data validation, search, Dash categories)
docs/                                        SPEC.md (requirements), TEAM_PLAN.md, CONTRACT.md
AGENTS.md                                    instructions for AI coding agents
AI_PROMPTS.txt                               log of the AI prompts used, per member
requirements.txt                             pinned dependencies for notebooks, tests and the Streamlit fallback
```

`data/` is git-ignored except `data/zip_year.csv` and `data/dummy_zip_year.csv`: the notebooks download their own raw data from the NYC Open Data API or read the previous notebook's output.

## Setup (VS Code + Python venv)

No Colab and no Google Drive: everything runs locally with relative paths. Tested with Python 3.14 on Windows (`.python-version` says 3.14).

```bash
# from the repository root
python -m venv .venv
.venv\Scripts\activate            # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

In VS Code install the **Python** and **Jupyter** extensions, open the folder, and choose the `.venv` interpreter (Ctrl+Shift+P, "Python: Select Interpreter"). Open a notebook, click **Select Kernel**, pick `.venv`, then **Restart** and **Run All**.

## Notebook run order

Run from the repository root. Housing and collision paths are independent until the join. Times are measured on one fresh clone of `main` (new venv) on the author's Windows PC with a normal home connection; the first runs download data from the API, so times vary.

| # | Notebook | Reads | Writes | Approx. run time |
|---|---|---|---|---|
| 1 | `phase1_housing_initial_cleaning_issa.ipynb` | NYC API (or `data/housing_raw.csv` cache) | `data/housing_raw.csv`, `data/housing_step1.csv.gz` | about 7 min (first run, downloads the data) |
| 2 | `phase1_housing_eda_cleaning_walid.ipynb` | `data/housing_step1.csv.gz` | `data/housing_step2.csv.gz` | under 1 min |
| 3 | `phase2_housing_zip_year_walid.ipynb` | `data/housing_step2.csv.gz` | `data/housing_zip_year.csv.gz` | under 1 min |
| 4 | `phase1_collisions_initial_cleaning_yassin.ipynb` | NYC API (or `data/collisions_raw.csv` cache) | `data/collisions_step1.csv.gz` (+ audit JSON) | about 4-5 min (first run, downloads the data) |
| 5 | `phase1_collisions_eda_cleaning_ahmed.ipynb` | NYC API (or `data/collisions_raw.csv` cache) | `data/collisions_raw.csv`, `data/collisions_step2.csv.gz` | about 11 min (first run, downloads the data) |
| 6 | `phase2_collisions_aggregation_yassin.ipynb` | `data/collisions_step2.csv.gz` | `data/collisions_zip_year.csv` | under 1 min |
| 7 | `phase2_data_integration_issa.ipynb` | the two ZIP x year files | `data/zip_year.csv` | under 1 min |
| 8 | `phase3_analysis_ahmed.ipynb` | `data/zip_year.csv` (and `data/collisions_step2.csv.gz` for one context cell) | `assets/rq/ahmed_q1.png`, `ahmed_q2.png` | under 1 min |
| 9 | `phase3_analysis_issa.ipynb` | `data/zip_year.csv` | `assets/rq/issa_q1.png`, `issa_q2.png` | under 1 min |
| 10 | `phase3_analysis_walid.ipynb` | `data/zip_year.csv` | `assets/rq/walid_q1.png`, `walid_q2.png` | under 1 min |
| 11 | `phase3_analysis_yassin.ipynb` | `data/zip_year.csv` | none (reads only; the research-question files for Yassin are committed under `assets/rq/`) | under 1 min |
| 12 | `00_project_overview.ipynb` | repository files | none (availability check and overview) | under 1 min |

Notes:
- Step 5 does its own raw pull and does not load step 4's export, so the upstream notebooks may not share an identical API snapshot.
- Re-running the API notebooks can change counts slightly even inside the 2022 onward window; the committed `data/zip_year.csv` is the reference table the website and the analyses use.
- Every notebook ends with a "Prompts used" cell that points to `AI_PROMPTS.txt`, and has a contribution note.

## Run the website locally

The website is a Dash app (Plotly charts) that reuses the logic in `src/`.

```bash
# from the repository root, with the venv active
python dash_app.py                # opens http://127.0.0.1:8050
```

Tabs:
- **Dashboard**: search box (for example `Brooklyn 2022 new buildings`), Borough / Year / Housing category / Collision category dropdowns, an optional ZIP multiselect, and the **Generate Report** button. Nothing on the page updates until the button is clicked. Four interactive charts: bar, line, scatter, grouped bar.
- **Research questions**: shows each member's question, chart and finding from `assets/rq/<name>_q<1|2>.md` and `.png`; a missing entry shows "not yet available".
- **Story**: the question, the data, the discoveries, the limits and the impact.

If `data/zip_year.csv` is missing the site falls back to `data/dummy_zip_year.csv` and shows a "Showing dummy data" banner. The housing categories "Alterations" and "Demolitions" are hidden (with a note) if `alteration_job_count` / `demolition_job_count` are absent.

Run the tests:

```bash
python -m pytest
```

The earlier Streamlit version still works: `streamlit run app.py` (http://localhost:8501). It is not what is deployed.

## Deployment (Vercel)

Vercel cannot run Streamlit (it needs a long-running server), so the deployed site is the Dash app. Vercel looks for a WSGI callable named `app`: `vercel_app.py` exposes the Flask object of the Dash app (`from dash_app import server as app`), and `pyproject.toml` points to it with `[tool.vercel] entrypoint = "vercel_app:app"`.

### Requirements exception (one file for notebooks, a lean list for the web function)

The team rule is one shared `requirements.txt`, and the notebooks, tests and the Streamlit fallback still use it. The Vercel function must not install notebook packages (jupyter, seaborn, nbconvert, pytest ...), so its web-only dependencies live in `pyproject.toml` (`dash==4.4.1`, `plotly==7.1.0`, `pandas==3.1.0`, `numpy==2.5.4`); the versions match `requirements.txt` where a package exists in both. `.python-version` selects Python 3.14. `vercel.json` excludes notebooks, tests, docs, scripts and `app.py` from the function bundle; `data/` and `assets/` are bundled because Vercel includes the files reachable in the project.

### Project settings

1. Import `Sanad-Manga/NYC-Build-And-Crash` as a new project in Vercel (signed in with GitHub).
2. Framework Preset: **Other**.
3. Root Directory: empty (repository root).
4. Build, Output and Install commands: no override (Vercel installs from `pyproject.toml`).
5. Environment variables: none.
6. Production Branch: **main**; every merge to `main` redeploys.

These are the settings in the repository's deployment notes. Whether the existing Vercel project was configured exactly this way is to be confirmed by Ahmed (the project was already present and building from `main` when the deployment was checked).

## Data contract for `data/zip_year.csv`

`src/data.py::validate()` checks the required columns; the app shows a clear error if the table is broken. The committed table has 1,123 rows (one per ZIP x year, 232 ZIP codes, years 2022 to 2026) and 25 columns.

| Column | Type | Rule |
|---|---|---|
| `zip_code` | string | exactly 5 digits, leading zeros kept (read with `dtype={"zip_code": str}`) |
| `year` | integer | 2022 to 2026 |
| `borough` | string | Manhattan, Brooklyn, Queens, Bronx or Staten Island |
| `housing_job_count` | integer | unique jobs started, from the initial I1 filings |
| `new_building_count` | integer | the same count, New Building jobs only |
| `collision_count` | integer | crashes with a valid ZIP |
| `persons_injured`, `persons_killed`, `pedestrians_injured`, `cyclist_injured`, `motorist_injured` | integer | injury and death counts |
| `is_partial_year` | boolean | True for 2026 (January to October) |
| `alteration_job_count`, `demolition_job_count` | integer | optional; the website hides the matching options if absent |

Rules: one row per `zip_code` x `year`; the required count columns are non-negative integers with no missing values; a ZIP x year present in only one source has 0 for the other source's counts (`match_status` says `both`, `housing only` or `collisions only`).

The table also carries extra columns added by the integration and cleaning notebooks, which the website ignores: `pedestrians_killed`, `cyclist_killed`, `motorist_killed`, `proposed_dwelling_units_new_buildings`, `top_contributing_factor`, `low_data_flag`, `outlier_flag`, `match_status`, `new_buildings_per_year_rank`, `injuries_per_100_collisions`, `extreme_injury_count`. `top_contributing_factor` and `injuries_per_100_collisions` have missing values (by design, for example where there are no collisions).

## Team contributions

Team of four; Ahmed Sanad is team leader. Contributions below come from `docs/TEAM_PLAN.md` and the merged pull requests (PR numbers are on GitHub); `git log` shows commits by all four members.

| Member | Phase 1 | Phase 2 | Phase 3 and website |
|---|---|---|---|
| **Ahmed Sanad** | Collisions EDA and cleaning (PR 3); prompt log (PR 2) | Website skeleton with filters, search and Generate Report (PR 8) | Analysis notebook and 2 research questions (PR 13); Dash website for Vercel (PR 16); Story and research-question fixes (PR 21, 23, 24); README |
| **Mohamed Issa** | Housing loading and initial cleaning (PR 6) | Integration, post-join cleaning and `data/zip_year.csv` (PR 12) | 2 research questions (PR 17) |
| **Mohamed Walid** | Housing EDA and cleaning (PR 1); team standards (PR 5) | Housing ZIP x year aggregation (PR 11) | 2 research questions (PR 18); deployment testing (to be confirmed by Walid) |
| **Yassin** | Collisions initial cleaning (PR 4, 15, 20) | Collisions ZIP x year aggregation (PR 10) | 2 research questions (PR 19); `00_project_overview.ipynb` (PR 22) |

## The eight research questions

Question wording is the first line of each `assets/rq/<name>_q<n>.md`; the findings and numbers are in those files and in the notebook named in the last column.

| Member | Question | Chart type | Notebook |
|---|---|---|---|
| Ahmed | Are ZIP codes with more new buildings also the ZIP codes where pedestrians and cyclists are hurt more often per collision? | Grouped bar, bootstrap 95% intervals | `phase3_analysis_ahmed.ipynb` |
| Ahmed | Do ZIP codes with the most new construction have a different mix of top contributing factors than ZIP codes with the least? | Horizontal stacked bar | `phase3_analysis_ahmed.ipynb` |
| Issa | Where is construction growing fastest, and do collisions in those ZIP codes move the same way? | Scatter | `phase3_analysis_issa.ipynb` |
| Issa | Does the borough pattern of construction match the borough pattern of collisions over time? | Heatmap | `phase3_analysis_issa.ipynb` |
| Walid | Is demolition activity in a ZIP code associated with more or fewer collisions per housing job? | Box plot with points | `phase3_analysis_walid.ipynb` |
| Walid | Do ZIP codes adding many planned dwelling units in new buildings have a different pedestrian injury rate than ZIP codes adding few? | Bubble scatter | `phase3_analysis_walid.ipynb` |
| Yassin | How deadly are the crashes in ZIP codes with a lot of new construction? | Grouped bar, bootstrap 95% intervals | `phase3_analysis_yassin.ipynb` |
| Yassin | Which boroughs account for a larger share of collisions than of construction, and has that changed? | Line chart | `phase3_analysis_yassin.ipynb` |

## Use of AI

All four members used AI assistants (Claude Code and others as logged) and recorded the prompts that shaped the submitted work in **`AI_PROMPTS.txt`** at the repository root, in the course format: date, student, tool, related requirement, prompt, and how the output was used. The log is append-only on `main`. `AGENTS.md` holds the instructions given to AI coding agents. Every notebook ends with a "Prompts used" cell.

## Limitations

- About 28% of collisions have no ZIP code and are excluded from ZIP-level counts; the share is higher in 2022 and 2023, so ZIP-level collision counts are undercounts and early years are less complete.
- 2026 is a partial year (January to October); never compare its totals with full years. Most full-year comparisons use 2022 to 2025.
- There is no traffic-volume or population data: a busy ZIP may simply have more cars and people, so counts are not rates of risk.
- ZIP codes are not neighborhoods, and they differ widely in size and land use.
- Housing records are job **filings**, not completed construction; proposed dwelling units are plans.
- Everything here is association between two datasets, not evidence that one causes the other.
