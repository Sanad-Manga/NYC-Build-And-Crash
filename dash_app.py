"""NYC Build and Crash: Dash website (runs on Vercel; the Streamlit app.py stays as a fallback).

Run locally from the repo root:  python dash_app.py   (then open http://127.0.0.1:8050)
Nothing on the Dashboard tab changes until "Generate Report" is clicked: the button is the only Input of the
report callback, every filter is a State. The logic lives in src/ (data, search, report, charts, research).
"""
from pathlib import Path

import pandas as pd
from dash import Dash, Input, Output, State, dcc, html, no_update

from src import charts
from src.data import (BOROUGHS, YEAR_MAX, YEAR_MIN, DataValidationError, is_dummy, load_data,
                      resolve_data_path)
from src.report import (COLLISION_CATEGORIES, HOUSING_CATEGORIES, apply_filters, available_categories,
                        filters_text, metric_label, summary)
from src.research import MEMBERS, NOT_AVAILABLE, scan_research
from src.search import describe_categories, parse_categories

BASE_DIR = Path(__file__).resolve().parent
ALL = "all"
YEARS = list(range(YEAR_MIN, YEAR_MAX + 1))

app = Dash(__name__, assets_folder=str(BASE_DIR / "assets"), title="NYC Build and Crash",
           suppress_callback_exceptions=True)
server = app.server          # the Flask (WSGI) object; vercel_app.py exposes it as `app`

# ---------------------------------------------------------------- data
DATA_PATH = resolve_data_path()
try:
    data = load_data(DATA_PATH)
    DATA_ERROR = None
except (DataValidationError, FileNotFoundError) as error:       # show a message instead of crashing
    data, DATA_ERROR = pd.DataFrame(), str(error)

HOUSING = available_categories(HOUSING_CATEGORIES, data.columns)
COLLISION = available_categories(COLLISION_CATEGORIES, data.columns)
MISSING_HOUSING = [label for label in HOUSING_CATEGORIES if label not in HOUSING]
ALL_ZIPS = sorted(data["zip_code"].unique()) if DATA_ERROR is None else []


def housing_label(column):
    return next((label for label, col in HOUSING.items() if col == column), column)


def collision_label(column):
    return next((label for label, col in COLLISION.items() if col == column), column)


# ---------------------------------------------------------------- layout helpers
def field(label, component, control_id, is_input=False):
    """A labelled control. Text input: <label for>. Dropdown: a group named by the label (Dash's dropdown
    button is named from its value, so the label would not be announced otherwise)."""
    label_id = f"{control_id}-label"
    if is_input:
        return html.Div([html.Label(label, id=label_id, htmlFor=control_id, className="lbl"), component],
                        className="field")
    return html.Div([html.Label(label, id=label_id, className="lbl"), component], className="field",
                    role="group", **{"aria-labelledby": label_id})


def dropdown(id_, options, value):
    return dcc.Dropdown(id=id_, options=options, value=value, clearable=False)


def build_filters():
    return html.Div([
        html.Div([
            field("Search mode", dcc.Input(id="search", type="text", debounce=True, className="search",
                                           placeholder="e.g. Brooklyn 2022 new buildings"),
                  "search", is_input=True),
            html.Div("Press Enter: the text sets the dropdowns below. Then click Generate Report.",
                     className="hint"),
            html.Div(id="search-msg", className="hint", role="status"),
        ], className="search-box"),
        html.Div([
            field("Borough", dropdown("borough", [{"label": "All boroughs", "value": ALL}] +
                                      [{"label": b, "value": b} for b in BOROUGHS], ALL),
                  "borough"),
            field("Year", dropdown("year", [{"label": "All years", "value": ALL}] +
                                   [{"label": f"{y} (partial, to 31 Oct)" if y == YEAR_MAX else str(y), "value": y}
                                    for y in YEARS], ALL), "year"),
            field("Housing category", dropdown("housing", [{"label": l, "value": c} for l, c in HOUSING.items()],
                                               "housing_job_count"), "housing"),
            field("Collision category", dropdown("collision", [{"label": l, "value": c} for l, c in COLLISION.items()],
                                                 "collision_count"), "collision"),
            field("ZIP codes (optional)", dcc.Dropdown(id="zips", options=ALL_ZIPS, value=[], multi=True,
                                                       placeholder="All ZIP codes"), "zips"),
        ], className="filter-row"),
        html.Div(f"Not available in this data, so hidden: {', '.join(MISSING_HOUSING)}.", className="hint warn")
        if MISSING_HOUSING else None,
    ], className="panel")


def dashboard_tab():
    return html.Div([
        build_filters(),
        html.Div(html.Button("Generate Report", id="generate", n_clicks=0, className="primary"),
                 className="center"),
        html.Div(id="stale-note", className="hint center", role="status"),
        dcc.Loading(html.Div(id="report", children=html.Div(
            "Choose filters (or type a search), then click Generate Report. Nothing below changes until you do.",
            className="info")), type="dot"),
    ])


def rq_card(entry):
    if entry["image"]:
        src = f"/assets/rq/{entry['image']}"
        image = html.Div([
            html.A(html.Img(src=src, className="rq-img",
                            alt=f"Chart for {entry['member']}, question {entry['number']}"),
                   href=src, target="_blank", rel="noopener",
                   title="Open the chart at full size in a new tab"),
            html.Div("Click the chart to open it at full size.", className="hint")])
    else:
        image = html.Div("Chart image: " + NOT_AVAILABLE, className="muted")
    finding = html.P(entry["finding"], className="finding") if entry["available"] else \
        html.P(NOT_AVAILABLE, className="muted")
    return html.Div([
        html.H2(f"{entry['member']}, question {entry['number']}", className="card-title"),
        html.P([html.B("Question: "), entry["question"]]),
        image,
        html.Div([html.B("Finding: "), finding], className="finding-box"),
    ], className="card", id=f"rq-{entry['name']}-q{entry['number']}")


def research_tab():
    entries = scan_research()
    ready = sum(e["available"] for e in entries)
    return html.Div([
        html.P(f"{ready} of {len(entries)} research questions are available. Each member answered two questions "
               "with one chart each. All findings describe association only, never cause and effect."),
        html.Div([rq_card(e) for e in entries], className="grid"),
    ])


def _finding(title, text, source):
    return html.Li([html.B(title + " "), text, html.Div(f"From: {source}", className="muted")])


def story_tab():
    """The data story: question, data, discovery, limits, impact. The discovery is a plain-language synthesis of
    the eight research answers (numbers taken from assets/rq/*.md); the full answers are on the Research tab."""
    return html.Div([
        html.Div([html.B("In one sentence: "),
                  "ZIP codes with a lot of construction also have a lot of collisions, but their crashes are not "
                  "clearly more injurious or deadly, so building activity and crash counts mostly rise together "
                  "with the size of the area."], className="story-summary"),
        html.Section([
            html.H2("1. The question, and why it matters to New Yorkers"),
            html.P("Do the ZIP codes where New York City sees the most building activity also see more motor vehicle "
                   "collisions, and more injuries to pedestrians, cyclists and motorists? Construction changes streets, "
                   "traffic and crowds, so the answer could help residents, planners and safety groups know where to "
                   "look first. We only ask about association."),
        ], className="story-sec"),
        html.Section([
            html.H2("2. The data"),
            html.P("Two NYC Open Data sets: building job filings (what is being built) and police-reported motor "
                   "vehicle crashes (what happens on the street). They share no record-level key, so we count each by "
                   "ZIP code and year and compare the counts: 1,123 ZIP-by-year rows, 232 ZIP codes, 375,144 housing "
                   "jobs started and 321,092 collisions in 2022 to 2026."),
            html.Ul([
                html.Li(html.A("DOB NOW: Build job application filings (NYC Open Data w9ak-ipjd)",
                               href="https://data.cityofnewyork.us/d/w9ak-ipjd", target="_blank", rel="noopener")),
                html.Li(html.A("Motor Vehicle Collisions, Crashes (NYC Open Data h9gi-nx95)",
                               href="https://data.cityofnewyork.us/d/h9gi-nx95", target="_blank", rel="noopener")),
            ]),
            html.P("Crashes without a ZIP code cannot be placed, so they are left out of the ZIP-level counts. How each "
                   "dataset was cleaned is in the Phase 1 and Phase 2 notebooks.", className="muted"),
        ], className="story-sec"),
        html.Section([
            html.H2("3. The discovery"),
            html.P("Five things stand out. The numbers come from the eight research questions; the charts and full "
                   "answers are on the Research questions tab.", className="muted"),
            html.Ol([
                _finding("More building goes with more crashes.",
                         "ZIP codes with more housing jobs started also have more collisions (correlation 0.54 on the "
                         "dashboard chart). Big, busy areas have both.",
                         "Dashboard scatter; Ahmed question 1"),
                _finding("But the crashes there are not worse.",
                         "In the ZIP codes with the most new buildings, 15.5 pedestrians and cyclists were injured per "
                         "100 collisions, against 21.4 in the ZIP codes with the fewest. Deaths per 1,000 collisions "
                         "were similar (2.18 against 2.40, intervals overlap), and the leading cause is the same: "
                         "driver inattention (89.8% against 94.8% of ZIP-years).",
                         "Ahmed questions 1 and 2, Yassin question 1"),
                _finding("Where construction grew, crashes did not follow.",
                         "From 2022 to 2025 the change in housing jobs and the change in collisions are weakly and "
                         "negatively related across 209 ZIP codes (rank correlation -0.22): growing ZIP codes, if "
                         "anything, saw collisions fall slightly.",
                         "Issa question 1"),
                _finding("Boroughs differ, and Brooklyn stands out.",
                         "Brooklyn has a larger share of the city's collisions than of its construction, about 10 "
                         "percentage points, in every year we looked at and under two different measures of construction.",
                         "Issa question 2, Yassin question 2"),
                _finding("Demolitions and planned housing add little.",
                         "ZIP codes with the most demolitions had a higher median collision rate per housing job "
                         "(118.22 against 101.21), but the uncertainty range includes zero. More planned dwelling "
                         "units go with a slightly higher pedestrian injury rate (rank correlation 0.24).",
                         "Walid questions 1 and 2"),
            ], className="takeaways"),
        ], className="story-sec"),
        html.Section([
            html.H2("4. The limits"),
            html.Ul([
                html.Li("About 28% of crashes have no ZIP code and are excluded, more of them in 2022 and 2023, so "
                        "ZIP-level collision counts are undercounts."),
                html.Li("2026 covers January to October only; never compare its totals with a full year."),
                html.Li("There is no traffic or population denominator: a busy ZIP may simply have more cars and "
                        "people."),
                html.Li("ZIP codes are not neighbourhoods, and filings are not completed construction."),
                html.Li("We can only describe association between the two datasets; nothing here shows cause and "
                        "effect."),
            ]),
        ], className="story-sec"),
        html.Section([
            html.H2("5. The impact"),
            html.P("Residents and community boards could use the report to see which ZIPs show high building activity "
                   "and high collision counts together. Planners and safety groups could look next at those ZIPs, "
                   "adding traffic counts and population to check whether the pattern holds. This is a starting point "
                   "for questions, not a claim that building causes crashes."),
        ], className="story-sec"),
    ])


def build_layout():
    if DATA_ERROR:
        return html.Div([html.H1("NYC Build and Crash"),
                         html.Div(f"Could not load the data: {DATA_ERROR}", className="banner", role="alert")],
                        className="page")
    banner = html.Div("Showing dummy data: every number is randomly generated for testing the layout. "
                      "It says nothing about the real city.", className="banner", role="alert") \
        if is_dummy(DATA_PATH) else None
    return html.Div([
        html.H1("NYC Build and Crash"),
        html.P("Do the ZIP codes with the most new construction also see more collisions? We compare ZIP-level "
               "patterns: correlation only, never proof of cause.", className="muted"),
        banner,
        dcc.Tabs(id="tabs", value="dash", children=[
            dcc.Tab(label="Dashboard", value="dash", children=dashboard_tab()),
            dcc.Tab(label="Research questions", value="rq", children=research_tab()),
            dcc.Tab(label="Story", value="story", children=story_tab()),
        ]),
    ], className="page")


app.layout = build_layout     # a function: the research-question files are re-scanned on every page load


# ---------------------------------------------------------------- callbacks
@app.callback(
    Output("borough", "value"), Output("year", "value"), Output("housing", "value"),
    Output("collision", "value"), Output("zips", "value"), Output("search-msg", "children"),
    Input("search", "value"), State("housing", "value"), State("collision", "value"),
    prevent_initial_call=True)
def apply_search(text, housing_now, collision_now):
    """Search box: set the dropdowns from the text. Nothing is drawn until Generate Report is clicked."""
    if not text or not text.strip():
        return no_update, no_update, no_update, no_update, no_update, ""
    parsed = parse_categories(text)
    notes = []
    housing, collision = housing_now, collision_now
    if parsed["housing"]:
        if parsed["housing"] in HOUSING.values():
            housing = parsed["housing"]
        else:
            notes.append(f"{parsed['housing'].replace('_job_count', '')} jobs are not in this data")
    if parsed["collision"]:
        collision = parsed["collision"]
    zips = []
    if parsed["zip_code"]:
        if parsed["zip_code"] in ALL_ZIPS:
            zips = [parsed["zip_code"]]
        else:
            notes.append(f"ZIP {parsed['zip_code']} is not in the data")
    understood, ignored = describe_categories(parsed)
    if understood == "nothing recognised":        # leave the dropdowns as they are
        return (no_update,) * 5 + (f"Understood: nothing recognised. Ignored: {ignored}.",)
    for label, column in {**HOUSING_CATEGORIES, **COLLISION_CATEGORIES}.items():   # show labels, not column names
        understood = understood.replace(f"= {column}", f"= {label}")
    msg = f"Understood: {understood}."
    if ignored:
        msg += f" Ignored: {ignored}."
    if notes:
        msg += " Also ignored: " + "; ".join(notes) + "."
    # a search describes the whole selection: parts not mentioned go back to "all"
    return parsed["borough"] or ALL, parsed["year"] or ALL, housing, collision, zips, msg


def _graph(fig, caption, id_):
    return html.Figure([dcc.Graph(figure=fig, id=id_, config={"displaylogo": False}),
                        html.Figcaption(caption, id=f"{id_}-caption", className="caption")],
                       className="chart", **{"aria-labelledby": f"{id_}-caption"})


def stat(value, label):
    return html.Div([html.Div(f"{value}", className="big"), html.Div(label)], className="stat")


@app.callback(Output("report", "children"), Output("stale-note", "children"),
              Input("generate", "n_clicks"),
              State("borough", "value"), State("year", "value"), State("housing", "value"),
              State("collision", "value"), State("zips", "value"),
              prevent_initial_call=True)
def generate_report(n_clicks, borough, year, housing, collision, zips):
    """The only trigger for the charts: the Generate Report button. Filters are read as State."""
    borough = None if borough in (None, ALL) else borough
    year = None if year in (None, ALL) else int(year)
    h = housing if housing in HOUSING.values() else "housing_job_count"
    c = collision if collision in COLLISION.values() else "collision_count"
    zl = sorted(zips or [])
    filtered = apply_filters(data, borough, year, zl)
    if filtered.empty:
        return html.Div("No data matches these filters. Try a different borough, year or ZIP.",
                        className="info"), ""
    stats, h_stats = summary(filtered, c), summary(filtered, h)
    cards = html.Div([
        stat(f"{h_stats['total']:,}", f"Total {metric_label(h).lower()}"),
        stat(f"{stats['total']:,}", f"Total {metric_label(c).lower()}"),
        stat(stats["zip_count"], "ZIP codes included"),
        stat(stats["top_zip"], f"Highest ZIP for {metric_label(c).lower()}"),
    ], className="stats")
    partial = html.P("Totals that include 2026 cover only January to October.", className="hint") \
        if stats["includes_partial_year"] else None
    trend_data = apply_filters(data, borough, None, zl)        # the trend always spans all years
    r, n = charts.pearson_r(filtered, h, c)
    r_text = f"Pearson r = {r:.2f} across {n} ZIPs" if r is not None else "too few ZIPs to compute a correlation"
    body = html.Div([
        _graph(charts.top_zips_bar(filtered, c),
               "The ZIP codes with the highest total for the collision category; colour shows the borough.",
               "chart-bar"),
        _graph(charts.trend_both(trend_data, h, c),
               "Yearly totals for the borough/ZIP filters (the year filter is ignored here). 2026 is partial "
               "(to 31 Oct), so its drop is not a real decline.", "chart-line"),
        _graph(charts.construction_vs_crashes(filtered, h, c),
               f"Each dot is one ZIP; counts are not normalised, so bigger ZIPs tend to have more of both. {r_text}. "
               "An association only, not evidence that one causes the other.", "chart-scatter"),
        _graph(charts.injuries_by_borough(filtered),
               "People injured, split by pedestrians, cyclists and motorists; ignores the collision category.",
               "chart-grouped"),
    ], className="grid")
    heading = html.H2(f"Report: {filters_text(borough, year, zl)}. "
                      f"Housing: {housing_label(h)}. Collisions: {collision_label(c)}.")
    return html.Div([heading, cards, partial, body]), ""


@app.callback(Output("stale-note", "children", allow_duplicate=True),
              Input("borough", "value"), Input("year", "value"), Input("housing", "value"),
              Input("collision", "value"), Input("zips", "value"),
              State("generate", "n_clicks"), prevent_initial_call=True)
def mark_stale(borough, year, housing, collision, zips, n_clicks):
    """Only a hint text: the charts themselves are never touched by the filters."""
    if not n_clicks:
        return ""
    return "The filters changed. Click Generate Report to update every chart."


if __name__ == "__main__":
    app.run(debug=False, port=8050)
