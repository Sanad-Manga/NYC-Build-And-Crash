"""NYC Build and Crash: Streamlit website skeleton.

Run from the repo root:  streamlit run app.py
Nothing on the page except the filter widgets changes until "Generate Report" is clicked.
The logic lives in src/ (data loading, search parsing, filtering, charts); this file only lays it out.
"""
import streamlit as st

from src import charts
from src.data import BOROUGHS, DataValidationError, YEAR_MAX, YEAR_MIN, is_dummy, load_data, resolve_data_path
from src.report import METRICS, apply_filters, filters_text, metric_label, summary
from src.search import describe_query, parse_query

ALL_BOROUGHS, ALL_YEARS = "All boroughs", "All years"
YEARS = list(range(YEAR_MIN, YEAR_MAX + 1))

st.set_page_config(page_title="NYC Build and Crash", layout="wide")


@st.cache_data
def get_data(path: str):
    """Load and validate the ZIP x year table once per file (cached between reruns)."""
    return load_data(path)


DATA_PATH = resolve_data_path()
try:
    data = get_data(str(DATA_PATH))
except (DataValidationError, FileNotFoundError) as error:      # show a clear message instead of a traceback
    st.error(f"Could not load the data: {error}")
    st.stop()
ALL_ZIPS = sorted(data["zip_code"].unique())

# ---------------------------------------------------------------- state
st.session_state.setdefault("f_borough", ALL_BOROUGHS)
st.session_state.setdefault("f_year", ALL_YEARS)
st.session_state.setdefault("f_metric", "collision_count")
st.session_state.setdefault("f_zips", [])
st.session_state.setdefault("applied", None)         # filters used by the last "Generate Report" click
st.session_state.setdefault("search_msg", None)


def apply_search():
    """Search box callback: parse the text and set the filter widgets (visuals do not change yet)."""
    text = st.session_state.get("f_search", "")
    if not text.strip():
        st.session_state["search_msg"] = None
        return
    parsed = parse_query(text)
    known_zips = set(get_data(str(DATA_PATH))["zip_code"])
    # a search describes the whole selection: parts not mentioned go back to "all"
    st.session_state["f_borough"] = parsed["borough"] or ALL_BOROUGHS
    st.session_state["f_year"] = parsed["year"] or ALL_YEARS
    if parsed["metric"]:
        st.session_state["f_metric"] = parsed["metric"]
    unknown_zip = None
    zip_code = parsed["zip_code"]
    if zip_code and zip_code in known_zips:
        st.session_state["f_zips"] = [zip_code]
    else:
        st.session_state["f_zips"] = []
        unknown_zip = zip_code
    understood, ignored = describe_query(parsed)
    st.session_state["search_msg"] = (understood, ignored, unknown_zip)


def current_selection() -> dict:
    """The filter widgets' current values as one comparable dict."""
    borough, year = st.session_state["f_borough"], st.session_state["f_year"]
    return {"borough": None if borough == ALL_BOROUGHS else borough,
            "year": None if year == ALL_YEARS else year,
            "metric": st.session_state["f_metric"],
            "zips": tuple(sorted(st.session_state["f_zips"]))}


# ---------------------------------------------------------------- sidebar: search + filters
st.sidebar.header("Search")
st.sidebar.text_input("Search mode", key="f_search", on_change=apply_search,
                      placeholder="e.g. Brooklyn 2022 new buildings")
st.sidebar.caption("Press Enter to turn the text into filters, then click Generate Report.")
if st.session_state["search_msg"]:
    understood, ignored, unknown_zip = st.session_state["search_msg"]
    st.sidebar.success(f"Understood: {understood}")
    if ignored:
        st.sidebar.warning(f"Ignored: {ignored}")
    if unknown_zip:
        st.sidebar.warning(f"ZIP {unknown_zip} is not in the data, so it was ignored.")

st.sidebar.header("Filters")
st.sidebar.selectbox("Borough", [ALL_BOROUGHS] + BOROUGHS, key="f_borough")
st.sidebar.selectbox("Year", [ALL_YEARS] + YEARS, key="f_year",
                     format_func=lambda y: f"{y} (partial, to 31 Oct)" if y == YEAR_MAX else str(y))
st.sidebar.selectbox("Metric", list(METRICS), key="f_metric", format_func=metric_label)
st.sidebar.multiselect("ZIP codes (optional)", ALL_ZIPS, key="f_zips")

# ---------------------------------------------------------------- header
st.title("NYC Build and Crash")
st.caption("Do the neighborhoods where NYC approves the most new construction also see more collisions? "
           "We compare ZIP-level patterns; this is correlation only, never proof of cause.")
if is_dummy(DATA_PATH):
    st.warning("**Showing dummy data**: `data/zip_year.csv` was not found, so every number on this page is randomly "
               "generated for testing the layout. It says nothing about the real city.", icon="⚠️")

_, middle, _ = st.columns([1, 2, 1])
generate = middle.button("Generate Report", type="primary", width="stretch")
if generate:
    st.session_state["applied"] = current_selection()

applied = st.session_state["applied"]


def render_report(sel: dict) -> None:
    """Draw the summary and all four charts for the filters that were applied."""
    metric = sel["metric"]
    zips = list(sel["zips"])
    filtered = apply_filters(data, sel["borough"], sel["year"], zips)
    if filtered.empty:
        st.warning("No data matches these filters. Try a different borough, year or ZIP.")
        return
    subtitle = filters_text(sel["borough"], sel["year"], zips)
    stats = summary(filtered, metric)

    st.subheader("Report summary")
    st.caption(f"Filters applied: {subtitle}. Metric: {metric_label(metric)}.")
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Total {metric_label(metric).lower()}", f"{stats['total']:,}")
    c2.metric("ZIP codes included", stats["zip_count"])
    c3.metric("Highest ZIP", stats["top_zip"])
    if stats["includes_partial_year"]:
        st.caption("Totals that include 2026 cover only January to October.")

    left, right = st.columns(2)
    with left:
        st.plotly_chart(charts.top_zips_bar(filtered, metric))
        st.caption("The ZIP codes with the highest total for the chosen metric; colour shows the borough.")
    with right:
        trend_data = apply_filters(data, sel["borough"], None, zips)      # trend always spans all years
        st.plotly_chart(charts.trend_line(trend_data, metric))
        st.caption("Yearly total for the borough/ZIP filters (the year filter is ignored here). "
                   "2026 is partial (to 31 Oct), so its drop is not a real decline.")

    left, right = st.columns(2)
    with left:
        st.plotly_chart(charts.construction_vs_crashes(filtered))
        r, n = charts.pearson_r(filtered)
        r_text = f"Pearson r = {r:.2f} across {n} ZIPs" if r is not None else "too few ZIPs to compute a correlation"
        st.caption(f"Each dot is one ZIP; counts are not normalised, so bigger ZIPs tend to have more of both. "
                   f"{r_text}. An association only, not evidence that one causes the other.")
    with right:
        st.plotly_chart(charts.injuries_by_borough(filtered))
        st.caption("People injured, split by pedestrians, cyclists and motorists; ignores the metric dropdown.")


st.divider()
if applied is None:
    st.info("Choose filters in the sidebar (or type a search), then click **Generate Report**.")
else:
    if applied != current_selection():
        st.info("The filters changed since the last report. Click **Generate Report** to update every chart.")
    render_report(applied)

# ---------------------------------------------------------------- story
st.divider()
st.header("Story")
st.markdown("""
**Question.** Do the neighborhoods (ZIP codes) where NYC sees the most new construction also have more
collisions, and more injuries to pedestrians, cyclists and motorists?

**Three hypotheses we will compare.**
(1) Construction goes together with more crashes.
(2) Construction happens in areas that were already busy, so both rise for the same reason.
(3) There is no clear relationship.

**Findings.** *The written findings are in `phase3_analysis_ahmed.ipynb`; the charts above show whatever table is loaded (see the banner when it is dummy data).*

**Limitations.**
- About 28% of collisions have no ZIP code, so ZIP-level collision counts are undercounts (more so in 2022-2023).
- 2026 is a partial year (data ends 31 Oct); never compare its totals with full years.
- There is no traffic-volume data: a busy ZIP may simply have more cars and people.
- Counts are not normalised by area or population.
- We can only describe association between the two datasets, not cause and effect.

**Benefit to NYC.** *Placeholder.* Planners could check street safety before approving large developments,
agencies could watch fast-growing ZIPs, and safety groups could focus on ZIPs where both measures are high.
""")
