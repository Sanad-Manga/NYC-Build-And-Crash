# NYC Build and Crash

Team project for **Data Engineering and Visualization** (German International University, Milestone 1, due 9 Nov 2026).

**Question.** Do the NYC neighborhoods (ZIP codes) with the most new construction also have more, or different, traffic collisions? We describe association only, never cause and effect.

- **Live website:** https://nyc-build-and-crash.vercel.app
- **Repository:** https://github.com/Sanad-Manga/NYC-Build-And-Crash
- **Entry-point notebook:** [00_project_overview.ipynb](00_project_overview.ipynb): dataset overview, integration explanation, findings, prompts used and dataset links. The other eleven notebooks (`phase1_*`, `phase2_*`, `phase3_*`) are its linked parts, one per cleaning, aggregation, integration or analysis step; each lists its own prompts and dataset links.

## Datasets

| Domain | Dataset | Link |
|---|---|---|
| Housing and Development | DOB NOW: Build - Job Application Filings (`w9ak-ipjd`) | https://data.cityofnewyork.us/d/w9ak-ipjd |
| Transportation | Motor Vehicle Collisions - Crashes (`h9gi-nx95`) | https://data.cityofnewyork.us/d/h9gi-nx95 |

The datasets share no row-level key, so each is aggregated to **ZIP code x year** and the two summaries are joined; individual filings are never matched to individual crashes. Scope is 2022-01-01 onward; 2026 is a partial year (to 31 Oct). The integrated table is `data/zip_year.csv` (1,123 rows, 232 ZIP codes), checked by `src/data.py::validate()`; its column contract is in `docs/CONTRACT.md`.

## Setup (VS Code + Python venv)

Everything runs locally with relative paths (no Colab, no Google Drive). Tested with Python 3.14 on Windows.

```bash
# from the repository root
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

In VS Code install the **Python** and **Jupyter** extensions and pick the `.venv` interpreter and kernel.

## Notebooks, in run order

Housing and collision paths are independent until the join. The first runs download data from the NYC Open Data API; the committed `data/zip_year.csv` is the reference table, so re-running the API notebooks may change counts slightly.

| # | Notebook | What it does | Approx. time |
|---|---|---|---|
| 1 | `phase1_housing_initial_cleaning_issa` | housing: loading, missing values, duplicates | about 7 min (downloads) |
| 2 | `phase1_housing_eda_cleaning_walid` | housing: EDA, outliers, ZIP/date standards | under 1 min |
| 3 | `phase2_housing_zip_year_walid` | housing aggregated to ZIP x year | under 1 min |
| 4 | `phase1_collisions_initial_cleaning_yassin` | collisions: initial cleaning and audit | about 4-5 min (downloads) |
| 5 | `phase1_collisions_eda_cleaning_ahmed` | collisions: EDA, ZIP/coordinate cleaning | about 11 min (downloads) |
| 6 | `phase2_collisions_aggregation_yassin` | collisions aggregated to ZIP x year | under 1 min |
| 7 | `phase2_data_integration_issa` | join, post-join cleaning, writes `data/zip_year.csv` | under 1 min |
| 8-11 | `phase3_analysis_ahmed`, `_issa`, `_walid`, `_yassin` | the eight research questions, charts in `assets/rq/` | under 1 min each |
| 12 | `00_project_overview` | overview and availability check | under 1 min |

Every notebook ends with a "Prompts used" cell pointing to `AI_PROMPTS.txt`. Do not re-run the Phase 3 notebooks of Issa or Walid before submitting: they rewrite `assets/rq/*.md` without the question line the website reads.

## Run the website and the tests

```bash
python dash_app.py        # http://127.0.0.1:8050
python -m pytest
```

Tabs: **Dashboard** (search box, Borough / Year / Housing category / Collision category dropdowns, optional ZIP selection, and one **Generate Report** button that updates everything), **Research questions** (each member's question, chart and finding from `assets/rq/`), and **Story** (question, data, discovery, limits, impact). If `data/zip_year.csv` is missing the site falls back to `data/dummy_zip_year.csv` and shows a "Showing dummy data" banner. The earlier Streamlit version (`streamlit run app.py`) is kept as a fallback and is not what is deployed.

## Deployment (Vercel)

Vercel cannot run Streamlit, so the deployed site is the Dash app: `vercel_app.py` exposes the Flask object of `dash_app.py` as `app`, and `pyproject.toml` points to it (`[tool.vercel] entrypoint = "vercel_app:app"`).

1. Import `Sanad-Manga/NYC-Build-And-Crash` as a new project in Vercel (signed in with GitHub).
2. Framework Preset **Other**; Root Directory empty; no build, output or install override; no environment variables.
3. Production branch **main**: every merge to `main` redeploys.

**One-file exception.** `requirements.txt` serves the notebooks, tests and Streamlit fallback. The Vercel function must not install notebook packages, so its web-only dependencies (`dash`, `plotly`, `pandas`, `numpy`, pinned to the same versions) live in `pyproject.toml`; `.python-version` selects Python 3.14 and `vercel.json` excludes notebooks, tests, docs and scripts from the bundle.

## Team contributions

Team of four; Ahmed Sanad is team leader. Source: `docs/TEAM_PLAN.md`, merged pull requests and `git log`.

| Member | Phase 1 | Phase 2 | Phase 3 and website |
|---|---|---|---|
| **Ahmed Sanad** | Collisions EDA and cleaning; prompt log | Website skeleton: filters, search, Generate Report | 2 research questions (grouped injury-rate bars; stacked contributing-factor profile); Dash website for Vercel with research and Story tabs; README |
| **Mohamed Issa** | Housing loading and initial cleaning | Integration, post-join cleaning, `data/zip_year.csv` | 2 research questions (change scatter with quadrants; borough-by-year diverging heatmap) |
| **Mohamed Walid** | Housing EDA and cleaning; team standards | Housing ZIP x year aggregation | 2 research questions (box plot of collisions per housing job; bubble scatter of planned dwelling units vs pedestrian injury rate); deployment testing (to be confirmed by Walid) |
| **Yassin Elshaer** | Collisions initial cleaning | Collisions ZIP x year aggregation | 2 research questions (grouped bars with bootstrap intervals; borough share lines); `00_project_overview.ipynb` |

## Use of AI

All four members used AI assistants and logged the prompts that shaped the submitted work in **`AI_PROMPTS.txt`** (date, student, tool, requirement, prompt, how the output was used). `AGENTS.md` holds the instructions given to AI coding agents.

## Limitations

- About 28% of collisions have no ZIP code and are excluded (more in 2022 and 2023), so ZIP-level collision counts are undercounts.
- 2026 is a partial year (January to October); never compare its totals with full years.
- No traffic-volume or population data: counts are not rates of risk. ZIP codes are not neighborhoods.
- Housing records are job filings, not completed construction.
- Everything here is association, not evidence of cause.
