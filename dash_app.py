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
from src.research import NOT_AVAILABLE, scan_research
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
def field(label, component):
    return html.Div([html.Label(label, className="lbl"), component], className="field")


def dropdown(id_, options, value):
    return dcc.Dropdown(id=id_, options=options, value=value, clearable=False)


def build_filters():
    return html.Div([
        html.Div([
            field("Search mode", dcc.Input(id="search", type="text", debounce=True, className="search",
                                           placeholder="e.g. Brooklyn 2022 new buildings")),
            html.Div("Press Enter: the text sets the dropdowns below. Then click Generate Report.",
                     className="hint"),
            html.Div(id="search-msg", className="hint", role="status"),
        ], className="search-box"),
        html.Div([
            field("Borough", dropdown("borough", [{"label": "All boroughs", "value": ALL}] +
                                      [{"label": b, "value": b} for b in BOROUGHS], ALL)),
            field("Year", dropdown("year", [{"label": "All years", "value": ALL}] +
                                   [{"label": f"{y} (partial, to 31 Oct)" if y == YEAR_MAX else str(y), "value": y}
                                    for y in YEARS], ALL)),
            field("Housing category", dropdown("housing", [{"label": l, "value": c} for l, c in HOUSING.items()],
                                               "housing_job_count")),
            field("Collision category", dropdown("collision", [{"label": l, "value": c} for l, c in COLLISION.items()],
                                                 "collision_count")),
            field("ZIP codes (optional)", dcc.Dropdown(id="zips", options=ALL_ZIPS, value=[], multi=True,
                                                       placeholder="All ZIP codes")),
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
        image = html.Img(src=f"/assets/rq/{entry['image']}", className="rq-img",
                         alt=f"Chart for {entry['member']}, question {entry['number']}")
    else:
        image = html.Div("Chart image: " + NOT_AVAILABLE, className="muted")
    finding = html.P(entry["finding"], className="finding") if entry["available"] else \
        html.P(NOT_AVAILABLE, className="muted")
    return html.Div([
        html.H4(f"{entry['member']}, question {entry['number']}"),
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


def story_tab():
    entries = [e for e in scan_research() if e["available"]][:5]
    if entries:
        discovery = html.Ul([html.Li([
            html.B(f"{e['member']}, question {e['number']}. "), e["question"], " ",
            html.Span(e["finding"].replace("\n", " "), className="finding"),
            html.Div(f"Source: assets/rq/{e['name']}_q{e['number']}.md, notebook "
                     f"phase3_analysis_{e['name']}.ipynb", className="muted")]) for e in entries])
    else:
        discovery = html.P("The findings will appear here once the research-question files are in assets/rq/. "
                           "Until then, nothing is claimed.", className="muted")
    return html.Div([
        html.H3("1. The question, and why it matters to New Yorkers"),
        html.P("Do the ZIP codes where New York City sees the most building activity also see more motor vehicle "
               "collisions, and more injuries to pedestrians, cyclists and motorists? Construction changes streets, "
               "traffic and crowds, so the answer could help residents, planners and safety groups know where to look "
               "first. We only ask about association."),
        html.H3("2. The data"),
        html.Ul([
            html.Li(html.A("DOB NOW: Build job application filings (NYC Open Data w9ak-ipjd)",
                           href="https://data.cityofnewyork.us/d/w9ak-ipjd", target="_blank", rel="noopener")),
            html.Li(html.A("Motor Vehicle Collisions, Crashes (NYC Open Data h9gi-nx95)",
                           href="https://data.cityofnewyork.us/d/h9gi-nx95", target="_blank", rel="noopener")),
        ]),
        html.P("Both datasets were cleaned in separate notebooks, then joined into one table with one row per "
               "ZIP code and year (2022 to 2026). Crashes without a ZIP code cannot be placed, so they are excluded "
               "from the ZIP-level counts; rows we could not use are described in the Phase 1 and Phase 2 notebooks."),
        html.H3("3. The discovery"),
        discovery,
        html.H3("4. The limits"),
        html.Ul([
            html.Li("About 28% of crashes have no ZIP code and are excluded, more of them in 2022 and 2023, so "
                    "ZIP-level collision counts are undercounts."),
            html.Li("2026 covers January to October only; never compare its totals with a full year."),
            html.Li("There is no traffic or population denominator: a busy ZIP may simply have more cars and people."),
            html.Li("ZIP codes are not neighbourhoods."),
            html.Li("Filings are not completed construction."),
            html.Li("We can only describe association between the two datasets; nothing here shows cause and effect."),
        ]),
        html.H3("5. The impact"),
        html.P("Residents and community boards could use the report to see which ZIPs show high building activity "
               "and high collision counts together. Planners and safety groups could look next at those ZIPs, "
               "adding traffic counts and population to check whether the pattern holds. This is a starting point "
               "for questions, not a claim that building causes crashes."),
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
    return html.Div([dcc.Graph(figure=fig, id=id_, config={"displaylogo": False}),
                     html.P(caption, className="caption")], className="chart")


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
    heading = html.H3(f"Report: {filters_text(borough, year, zl)}. "
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
