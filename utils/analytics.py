"""
utils/analytics.py
------------------
Pure-Python analytics helpers – no Streamlit dependency.
"""

import pandas as pd
import numpy as np
from utils.preprocessing import EXPENSE_COLS, POTENTIAL_SAVINGS_COLS


# ── Insight generation ──────────────────────────────────────────────────────

def generate_insights(df: pd.DataFrame) -> list[dict]:
    """
    Returns a list of insight dicts:
      { "icon": str, "title": str, "body": str, "type": "good"|"warn"|"info" }
    """
    insights = []
    present_exp = [c for c in EXPENSE_COLS if c in df.columns]

    # 1. Highest spending category
    if present_exp:
        cat_means = df[present_exp].mean()
        top_cat   = cat_means.idxmax()
        top_val   = cat_means.max()
        pct       = (top_val / df["Income"].mean() * 100).round(1)
        insights.append({
            "icon": "🏆", "type": "warn",
            "title": f"Top Expense: {top_cat.replace('_',' ')}",
            "body": f"Average ₹{top_val:,.0f}/month — {pct}% of income."
        })

    # 2. Savings gap
    if "Savings_Gap" in df.columns:
        avg_gap = df["Savings_Gap"].mean()
        if avg_gap > 0:
            insights.append({
                "icon": "⚠️", "type": "warn",
                "title": "Savings Shortfall Detected",
                "body": f"On average, users fall ₹{avg_gap:,.0f} short of their savings goal each month."
            })
        else:
            insights.append({
                "icon": "✅", "type": "good",
                "title": "Savings Goals Being Met",
                "body": f"Users exceed their savings target by ₹{abs(avg_gap):,.0f} on average — great discipline!"
            })

    # 3. Potential savings opportunity
    present_ps = [c for c in POTENTIAL_SAVINGS_COLS if c in df.columns]
    if present_ps:
        best_ps_col = df[present_ps].mean().idxmax()
        best_ps_val = df[present_ps].mean().max()
        label = best_ps_col.replace("Potential_Savings_","").replace("_"," ")
        insights.append({
            "icon": "💡", "type": "info",
            "title": f"Biggest Saving Opportunity: {label}",
            "body": f"Average potential saving of ₹{best_ps_val:,.0f}/month in {label}."
        })

    # 4. Expense-to-income ratio
    if "Expense_to_Income_%" in df.columns:
        avg_ratio = df["Expense_to_Income_%"].mean()
        t = "warn" if avg_ratio > 75 else "good"
        insights.append({
            "icon": "📊", "type": t,
            "title": f"Expense Ratio: {avg_ratio:.1f}%",
            "body": ("Expenses consume over 75% of income — consider cost reduction."
                     if avg_ratio > 75
                     else "A healthy expense ratio, leaving room for savings and investment.")
        })

    # 5. Age vs savings
    if "Age" in df.columns and "Savings_Rate_%" in df.columns:
        young = df[df["Age"] < 35]["Savings_Rate_%"].mean()
        senior = df[df["Age"] >= 35]["Savings_Rate_%"].mean()
        diff = round(senior - young, 1)
        insights.append({
            "icon": "📈", "type": "info",
            "title": "Age & Savings Pattern",
            "body": (f"Under-35s save {abs(diff)}% {'less' if diff > 0 else 'more'} "
                     f"than those 35+ ({young:.1f}% vs {senior:.1f}%).")
        })

    return insights


# ── Descriptive statistics ───────────────────────────────────────────────────

def top_level_kpis(df: pd.DataFrame) -> dict:
    kpis = {}
    kpis["total_records"]     = len(df)
    kpis["avg_income"]        = df["Income"].mean()            if "Income"        in df.columns else 0
    kpis["avg_expenses"]      = df["Total_Expenses"].mean()    if "Total_Expenses" in df.columns else 0
    kpis["avg_savings_rate"]  = df["Savings_Rate_%"].mean()    if "Savings_Rate_%" in df.columns else 0
    kpis["avg_disposable"]    = df["Disposable_Income"].mean() if "Disposable_Income" in df.columns else 0
    kpis["avg_potential_savings"] = (df["Total_Potential_Savings"].mean()
                                      if "Total_Potential_Savings" in df.columns else 0)
    return {k: round(v, 2) for k, v in kpis.items()}


def age_bucket_analysis(df: pd.DataFrame) -> pd.DataFrame:
    if "Age" not in df.columns:
        return pd.DataFrame()
    bins   = [20, 30, 40, 50, 65]
    labels = ["20-29", "30-39", "40-49", "50-64"]
    df2    = df.copy()
    df2["Age_Group"] = pd.cut(df2["Age"], bins=bins, labels=labels, right=False)
    return (df2.groupby("Age_Group", observed=True)
               .agg(Avg_Income=("Income","mean"),
                    Avg_Expenses=("Total_Expenses","mean"),
                    Avg_Savings_Rate=("Savings_Rate_%","mean"),
                    Count=("Income","count"))
               .round(2)
               .reset_index())
