"""
utils/visualizations.py
-----------------------
All Plotly chart factories used by the Streamlit dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.preprocessing import EXPENSE_COLS

# ── Brand palette ────────────────────────────────────────────────────────────
PRIMARY   = "#00C9A7"
SECONDARY = "#845EC2"
ACCENT    = "#FF6F91"
BG        = "#0D1117"
SURFACE   = "#161B22"
TEXT      = "#E6EDF3"

CATEGORY_COLORS = [
    "#00C9A7","#845EC2","#FF6F91","#FFC75F","#F9F871",
    "#00B8D9","#FF9671","#D65DB1","#4ECDC4","#A8E6CF","#FF8B94",
]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="'DM Sans', sans-serif", color=TEXT, size=13),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_color=TEXT),
)


def _apply(fig):
    fig.update_layout(**CHART_LAYOUT)
    return fig


# ── Charts ───────────────────────────────────────────────────────────────────

def expense_pie(df: pd.DataFrame) -> go.Figure:
    """Pie chart of average spending by category."""
    present = [c for c in EXPENSE_COLS if c in df.columns]
    values  = df[present].mean().values
    labels  = [c.replace("_", " ") for c in present]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=CATEGORY_COLORS, line=dict(color=BG, width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color=TEXT),
        hovertemplate="<b>%{label}</b><br>Avg ₹%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(title="💸 Expense Breakdown (Average)", **CHART_LAYOUT)
    return fig


def income_vs_expense_bar(df: pd.DataFrame, group_col: str = "City_Tier") -> go.Figure:
    """Grouped bar: Avg Income vs Avg Expenses by a categorical column."""
    if group_col not in df.columns:
        return go.Figure()
    grp = df.groupby(group_col)[["Income", "Total_Expenses"]].mean().round(0).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Income", x=grp[group_col], y=grp["Income"],
        marker_color=PRIMARY,
        hovertemplate="₹%{y:,.0f}<extra>Income</extra>",
    ))
    fig.add_trace(go.Bar(
        name="Expenses", x=grp[group_col], y=grp["Total_Expenses"],
        marker_color=ACCENT,
        hovertemplate="₹%{y:,.0f}<extra>Expenses</extra>",
    ))
    fig.update_layout(
        title=f"📊 Income vs Expenses by {group_col.replace('_',' ')}",
        barmode="group",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)"),
        **CHART_LAYOUT,
    )
    return fig


def savings_rate_histogram(df: pd.DataFrame) -> go.Figure:
    """Distribution of individual savings rates."""
    if "Savings_Rate_%" not in df.columns:
        return go.Figure()
    fig = go.Figure(go.Histogram(
        x=df["Savings_Rate_%"],
        nbinsx=30,
        marker_color=SECONDARY,
        opacity=0.85,
        hovertemplate="Rate: %{x:.1f}%<br>Count: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title="📉 Savings Rate Distribution",
        xaxis_title="Savings Rate (%)",
        yaxis_title="Count",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        **CHART_LAYOUT,
    )
    return fig


def expense_heatmap(df: pd.DataFrame) -> go.Figure:
    """Correlation heatmap of expense categories."""
    present = [c for c in EXPENSE_COLS if c in df.columns]
    corr    = df[present].corr().round(2)
    labels  = [c.replace("_", " ") for c in corr.columns]

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels, y=labels,
        colorscale=[[0, "#1a0533"], [0.5, "#845EC2"], [1, "#00C9A7"]],
        zmid=0,
        text=corr.values,
        texttemplate="%{text}",
        hovertemplate="<b>%{x}</b> × <b>%{y}</b><br>r = %{z}<extra></extra>",
    ))
    fig.update_layout(
        title="🔥 Expense Correlation Matrix",
        height=480,
        **CHART_LAYOUT,
    )
    return fig


def age_group_line(age_df: pd.DataFrame) -> go.Figure:
    """Line chart: income, expenses, savings rate by age bucket."""
    if age_df.empty:
        return go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        name="Avg Income",   x=age_df["Age_Group"], y=age_df["Avg_Income"],
        marker_color=PRIMARY, opacity=0.7,
        hovertemplate="₹%{y:,.0f}<extra>Income</extra>",
    ), secondary_y=False)
    fig.add_trace(go.Bar(
        name="Avg Expenses", x=age_df["Age_Group"], y=age_df["Avg_Expenses"],
        marker_color=ACCENT,  opacity=0.7,
        hovertemplate="₹%{y:,.0f}<extra>Expenses</extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        name="Savings Rate %", x=age_df["Age_Group"], y=age_df["Avg_Savings_Rate"],
        mode="lines+markers",
        line=dict(color=SECONDARY, width=3),
        marker=dict(size=9, color=SECONDARY),
        hovertemplate="%{y:.1f}%<extra>Savings Rate</extra>",
    ), secondary_y=True)

    fig.update_layout(
        title="📅 Financial Profile by Age Group",
        barmode="group",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        **CHART_LAYOUT,
    )
    fig.update_yaxes(title_text="Amount (₹)", secondary_y=False, gridcolor="rgba(255,255,255,0.07)")
    fig.update_yaxes(title_text="Savings Rate (%)", secondary_y=True, showgrid=False)
    return fig


def potential_savings_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar: average potential savings per category."""
    ps_cols = [c for c in df.columns if c.startswith("Potential_Savings_")]
    if not ps_cols:
        return go.Figure()

    means  = df[ps_cols].mean().sort_values()
    labels = [c.replace("Potential_Savings_","").replace("_"," ") for c in means.index]

    fig = go.Figure(go.Bar(
        x=means.values, y=labels,
        orientation="h",
        marker=dict(
            color=means.values,
            colorscale=[[0,"#1a0533"],[0.5,"#845EC2"],[1,"#00C9A7"]],
            showscale=False,
        ),
        hovertemplate="₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title="💡 Average Potential Savings by Category",
        xaxis_title="Amount (₹)",
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(showgrid=False),
        height=360,
        **CHART_LAYOUT,
    )
    return fig


def scatter_income_savings(df: pd.DataFrame, color_col: str = "City_Tier") -> go.Figure:
    """Scatter: Income vs Savings Rate, coloured by category."""
    if "Savings_Rate_%" not in df.columns or color_col not in df.columns:
        return go.Figure()

    fig = px.scatter(
        df, x="Income", y="Savings_Rate_%",
        color=color_col,
        color_discrete_sequence=CATEGORY_COLORS,
        opacity=0.65,
        hover_data={"Income":":.0f", "Savings_Rate_%":":.1f"},
        labels={"Income":"Monthly Income (₹)", "Savings_Rate_%":"Savings Rate (%)"},
        title=f"🔵 Income vs Savings Rate  [{color_col.replace('_',' ')}]",
    )
    fig.update_traces(marker_size=7)
    fig.update_layout(
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        **CHART_LAYOUT,
    )
    return fig


def occupation_bar(occ_df: pd.DataFrame) -> go.Figure:
    if occ_df.empty:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Avg Income",   x=occ_df["Occupation"], y=occ_df["Avg_Income"],
                         marker_color=PRIMARY, hovertemplate="₹%{y:,.0f}<extra>Income</extra>"))
    fig.add_trace(go.Bar(name="Avg Expenses", x=occ_df["Occupation"], y=occ_df["Avg_Expenses"],
                         marker_color=ACCENT,  hovertemplate="₹%{y:,.0f}<extra>Expenses</extra>"))
    fig.update_layout(
        title="💼 Income & Expenses by Occupation",
        barmode="group",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        **CHART_LAYOUT,
    )
    return fig
