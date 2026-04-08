"""
FinSight: Intelligent Personal Finance Analyzer
================================================
Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd

from utils.preprocessing import (
    load_and_validate, engineer_features,
    category_summary, city_tier_summary, occupation_summary,
)
from utils.analytics import (
    generate_insights, top_level_kpis, age_bucket_analysis,
)
from utils.visualizations import (
    expense_pie, income_vs_expense_bar, savings_rate_histogram,
    expense_heatmap, age_group_line, potential_savings_bar,
    scatter_income_savings, occupation_bar,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg:        #0D1117;
    --surface:   #161B22;
    --surface2:  #1C2333;
    --border:    #30363D;
    --primary:   #00C9A7;
    --secondary: #845EC2;
    --accent:    #FF6F91;
    --warn:      #FFC75F;
    --text:      #E6EDF3;
    --muted:     #8B949E;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--primary) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.5rem !important;
}

/* Section headings */
h1, h2, h3 { color: var(--text) !important; }

/* Dividers */
hr { border-color: var(--border) !important; }

/* Tabs */
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-baseweb="tab"] {
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--primary) !important;
    color: #0D1117 !important;
}

/* Data table */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_inr(val: float) -> str:
    if val >= 1_00_000:
        return f"₹{val/1_00_000:.2f}L"
    if val >= 1_000:
        return f"₹{val/1_000:.1f}K"
    return f"₹{val:.0f}"


def insight_card(icon, title, body, kind="info"):
    colours = {"good": "#00C9A7", "warn": "#FFC75F", "info": "#845EC2"}
    border  = colours.get(kind, "#845EC2")
    st.markdown(f"""
    <div style="background:#161B22;border-left:4px solid {border};
                border-radius:8px;padding:14px 18px;margin-bottom:10px;">
        <div style="font-size:1.1rem;font-weight:600;color:#E6EDF3;margin-bottom:4px;">
            {icon} {title}
        </div>
        <div style="color:#8B949E;font-size:0.88rem;line-height:1.5;">{body}</div>
    </div>""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:2.2rem;">💹</div>
        <div style="font-family:'Space Mono',monospace;font-size:1.3rem;
                    font-weight:700;color:#00C9A7;letter-spacing:0.05em;">FinSight</div>
        <div style="color:#8B949E;font-size:0.78rem;margin-top:4px;">
            Intelligent Finance Analyzer
        </div>
    </div>
    <hr style="border-color:#30363D;margin:10px 0 20px;">
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("📂 Upload CSV", type=["csv"],
                                help="Upload a finance dataset with expense columns.")

    st.markdown("---")
    st.markdown("**🔧 Filters**")

    # Placeholders — populated after data loads
    city_filter = []
    occ_filter  = []

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Processing data…")
def get_data(file_obj_or_path):
    raw = load_and_validate(file_obj_or_path)
    return engineer_features(raw)


if uploaded is not None:
    df_full = get_data(uploaded)
else:
    try:
        df_full = get_data("finance_data.csv")
        st.sidebar.info("ℹ️ Using sample dataset. Upload your own CSV above.", icon="📋")
    except FileNotFoundError:
        st.error("No data found. Please upload a CSV file or run `python generate_data.py` first.")
        st.stop()

# ── Sidebar filters (populated now) ──────────────────────────────────────────
with st.sidebar:
    if "City_Tier" in df_full.columns:
        all_cities = sorted(df_full["City_Tier"].dropna().unique())
        city_filter = st.multiselect("🏙️ City Tier", all_cities, default=all_cities)
    if "Occupation" in df_full.columns:
        all_occs = sorted(df_full["Occupation"].dropna().unique())
        occ_filter = st.multiselect("💼 Occupation", all_occs, default=all_occs)

    age_range = st.slider("🎂 Age Range", 20, 65, (20, 65))

    st.markdown("---")
    st.markdown(f"""
    <div style="color:#8B949E;font-size:0.75rem;text-align:center;">
        Dataset: {len(df_full):,} records &nbsp;|&nbsp; 27 features
    </div>""", unsafe_allow_html=True)

# Apply filters
df = df_full.copy()
if city_filter and "City_Tier" in df.columns:
    df = df[df["City_Tier"].isin(city_filter)]
if occ_filter and "Occupation" in df.columns:
    df = df[df["Occupation"].isin(occ_filter)]
if "Age" in df.columns:
    df = df[df["Age"].between(*age_range)]

if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust sidebar selections.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
kpis = top_level_kpis(df)

st.markdown("""
<h1 style="font-family:'Space Mono',monospace;font-size:1.8rem;
           letter-spacing:-0.02em;margin-bottom:4px;">
    💹 FinSight Dashboard
</h1>
<p style="color:#8B949E;margin-bottom:24px;">
    Indian Personal Finance & Spending Habits &nbsp;·&nbsp; Interactive Analysis
</p>""", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("👥 Records",        f"{kpis['total_records']:,}")
c2.metric("💰 Avg Income",     fmt_inr(kpis["avg_income"]))
c3.metric("💸 Avg Expenses",   fmt_inr(kpis["avg_expenses"]))
c4.metric("🏦 Savings Rate",   f"{kpis['avg_savings_rate']:.1f}%")
c5.metric("🔓 Disposable",     fmt_inr(kpis["avg_disposable"]))
c6.metric("💡 Pot. Savings",   fmt_inr(kpis["avg_potential_savings"]))

st.markdown("<hr>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
TAB_OVERVIEW, TAB_SPENDING, TAB_SAVINGS, TAB_DEMOGRAPHICS, TAB_DATA = st.tabs([
    "🏠 Overview", "💳 Spending", "📈 Savings & Goals", "🌍 Demographics", "🗃️ Raw Data"
])

# ─────────────── TAB 1: OVERVIEW ────────────────────────────────────────────
with TAB_OVERVIEW:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("### Expense Breakdown")
        st.plotly_chart(expense_pie(df), use_container_width=True)

    with col_b:
        st.markdown("### 🔍 Key Insights")
        insights = generate_insights(df)
        for ins in insights:
            insight_card(ins["icon"], ins["title"], ins["body"], ins["type"])

    st.markdown("---")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(income_vs_expense_bar(df, "City_Tier"), use_container_width=True)
    with right:
        st.plotly_chart(savings_rate_histogram(df), use_container_width=True)


# ─────────────── TAB 2: SPENDING ─────────────────────────────────────────────
with TAB_SPENDING:
    st.plotly_chart(expense_heatmap(df), use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(potential_savings_bar(df), use_container_width=True)
    with col2:
        cat_df = category_summary(df)
        st.markdown("### 📋 Category Spend Ranking")
        # Simple styled table
        cat_df["Avg_Spend"] = cat_df["Avg_Spend"].map(lambda v: f"₹{v:,.0f}")
        st.dataframe(cat_df, use_container_width=True, hide_index=True,
                     column_config={"Category": "Category", "Avg_Spend": "Avg Monthly Spend"})


# ─────────────── TAB 3: SAVINGS & GOALS ──────────────────────────────────────
with TAB_SAVINGS:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(scatter_income_savings(df, "City_Tier"), use_container_width=True)
    with col2:
        st.plotly_chart(scatter_income_savings(df, "Occupation"), use_container_width=True)

    st.markdown("---")
    # Savings gap summary
    if "Savings_Gap" in df.columns:
        gap_pos = df[df["Savings_Gap"] > 0]
        gap_neg = df[df["Savings_Gap"] <= 0]
        g1, g2, g3 = st.columns(3)
        g1.metric("🎯 Meeting Savings Goal",  f"{len(gap_neg)/len(df)*100:.0f}%")
        g2.metric("⚠️ Missing Savings Goal",   f"{len(gap_pos)/len(df)*100:.0f}%")
        g3.metric("📊 Avg Shortfall",           fmt_inr(df["Savings_Gap"].clip(0).mean()))


# ─────────────── TAB 4: DEMOGRAPHICS ─────────────────────────────────────────
with TAB_DEMOGRAPHICS:
    age_df = age_bucket_analysis(df)
    st.plotly_chart(age_group_line(age_df), use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        occ_df = occupation_summary(df)
        st.plotly_chart(occupation_bar(occ_df), use_container_width=True)
    with col2:
        city_df = city_tier_summary(df)
        if not city_df.empty:
            st.markdown("### 🏙️ City Tier Snapshot")
            city_df["Avg_Income"]    = city_df["Avg_Income"].map(lambda v: f"₹{v:,.0f}")
            city_df["Avg_Expenses"]  = city_df["Avg_Expenses"].map(lambda v: f"₹{v:,.0f}")
            city_df["Avg_Savings_Rate"] = city_df["Avg_Savings_Rate"].map(lambda v: f"{v:.1f}%")
            st.dataframe(city_df, use_container_width=True, hide_index=True)


# ─────────────── TAB 5: RAW DATA ─────────────────────────────────────────────
with TAB_DATA:
    st.markdown(f"**{len(df):,} rows** match current filters.")
    cols_to_show = [c for c in df.columns if not c.startswith("Potential_Savings_")]
    st.dataframe(df[cols_to_show].reset_index(drop=True),
                 use_container_width=True, height=450)

    csv_bytes = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download Filtered Data (CSV)", csv_bytes,
                       "finsight_filtered.csv", "text/csv")
