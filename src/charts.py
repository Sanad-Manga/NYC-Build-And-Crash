"""Plotly figures for the website. Every function takes an already-filtered ZIP x year table."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data import BOROUGHS, YEAR_MAX
from src.report import axis_title, metric_label

BOROUGH_COLORS = {"Manhattan": "#59a14f", "Brooklyn": "#4e79a7", "Queens": "#f28e2b",
                  "Bronx": "#e15759", "Staten Island": "#b07aa1"}
TEMPLATE = "plotly_white"


def _style(fig: go.Figure) -> go.Figure:
    """Shared layout: legend below the plot (keeps the plot area wide) and a compact title."""
    fig.update_layout(legend={"orientation": "h", "yanchor": "top", "y": -0.28, "x": 0, "title": None},
                      title={"font": {"size": 16}}, margin={"t": 60, "r": 20})
    return fig


def top_zips_bar(df: pd.DataFrame, metric: str, n: int = 10) -> go.Figure:
    """(a) Horizontal bar of the top-n ZIPs for the chosen metric (summed over the filtered years)."""
    top = (df.groupby(["zip_code", "borough"], as_index=False)[metric].sum()
             .nlargest(n, metric).sort_values(metric))
    fig = px.bar(top, x=metric, y="zip_code", orientation="h", color="borough",
                 color_discrete_map=BOROUGH_COLORS, template=TEMPLATE,
                 hover_data={"borough": True, "zip_code": True, metric: ":,"},
                 labels={metric: axis_title(metric), "zip_code": "ZIP code", "borough": "Borough"},
                 title=f"Top {len(top)} ZIP codes: {metric_label(metric).lower()}")
    fig.update_yaxes(type="category")
    return _style(fig)


def trend_line(df: pd.DataFrame, metric: str) -> go.Figure:
    """(b) Total of the metric per year; the partial last year is drawn dashed and hollow."""
    yearly = df.groupby("year", as_index=False)[metric].sum().sort_values("year")
    full, partial = yearly[yearly["year"] < YEAR_MAX], yearly[yearly["year"] == YEAR_MAX]
    fig = go.Figure()
    fig.add_scatter(x=full["year"], y=full[metric], mode="lines+markers", name="Full year",
                    line={"color": "#4e79a7"}, hovertemplate="%{x}: %{y:,}<extra></extra>")
    if not partial.empty:
        if not full.empty:       # dashed connector from the last full year to the partial year
            fig.add_scatter(x=[full["year"].iloc[-1], YEAR_MAX], y=[full[metric].iloc[-1], partial[metric].iloc[0]],
                            mode="lines", line={"color": "#4e79a7", "dash": "dash"}, showlegend=False,
                            hoverinfo="skip")
        fig.add_scatter(x=partial["year"], y=partial[metric], mode="markers", name="2026 (partial, to 31 Oct)",
                        marker={"color": "white", "line": {"color": "#4e79a7", "width": 2}, "size": 11},
                        hovertemplate="%{x} (partial): %{y:,}<extra></extra>")
    fig.update_layout(template=TEMPLATE, title=f"{metric_label(metric)} per year",
                      xaxis={"title": "Year", "dtick": 1}, yaxis={"title": axis_title(metric), "rangemode": "tozero"})
    return _style(fig)


def pearson_r(df: pd.DataFrame):
    """Pearson correlation of per-ZIP new-building jobs and collisions, plus the number of ZIPs."""
    per_zip = df.groupby("zip_code")[["new_building_count", "collision_count"]].sum()
    if len(per_zip) < 3 or per_zip.std().eq(0).any():
        return None, len(per_zip)
    return float(per_zip["new_building_count"].corr(per_zip["collision_count"])), len(per_zip)


def construction_vs_crashes(df: pd.DataFrame) -> go.Figure:
    """(c) Relationship between the two domains: new-building jobs vs collisions, one dot per ZIP."""
    per_zip = df.groupby(["zip_code", "borough"], as_index=False)[["new_building_count", "collision_count"]].sum()
    fig = px.scatter(per_zip, x="new_building_count", y="collision_count", color="borough",
                     color_discrete_map=BOROUGH_COLORS, template=TEMPLATE,
                     hover_name="zip_code", hover_data={"borough": True, "zip_code": False},
                     labels={"new_building_count": "New-building jobs started (count per ZIP)",
                             "collision_count": "Collisions (count per ZIP)", "borough": "Borough"},
                     title="New-building jobs vs collisions")
    fig.update_traces(marker={"size": 9, "opacity": 0.8})
    return _style(fig)


def injuries_by_borough(df: pd.DataFrame) -> go.Figure:
    """(d) Grouped bar: injuries by road-user type in each borough."""
    cols = {"pedestrians_injured": "Pedestrians", "cyclist_injured": "Cyclists", "motorist_injured": "Motorists"}
    by_borough = df.groupby("borough")[list(cols)].sum().reindex(BOROUGHS).dropna(how="all").reset_index()
    long = by_borough.melt(id_vars="borough", var_name="road_user", value_name="injured")
    long["road_user"] = long["road_user"].map(cols)
    fig = px.bar(long, x="borough", y="injured", color="road_user", barmode="group", template=TEMPLATE,
                  color_discrete_sequence=["#e15759", "#59a14f", "#4e79a7"],
                  labels={"borough": "Borough", "injured": "People injured (count)", "road_user": "Road user"},
                  title="Injuries by road user and borough")
    return _style(fig)
