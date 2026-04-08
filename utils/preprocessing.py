"""
utils/preprocessing.py
-----------------------
Data loading, validation, and feature engineering for FinSight.
"""

import pandas as pd
import numpy as np

EXPENSE_COLS = [
    "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport",
    "Eating_Out", "Entertainment", "Utilities", "Healthcare",
    "Education", "Miscellaneous",
]

POTENTIAL_SAVINGS_COLS = [c for c in [
    "Potential_Savings_Groceries", "Potential_Savings_Transport",
    "Potential_Savings_Eating_Out", "Potential_Savings_Entertainment",
    "Potential_Savings_Utilities", "Potential_Savings_Healthcare",
    "Potential_Savings_Education", "Potential_Savings_Miscellaneous",
]]


def load_and_validate(path_or_buffer) -> pd.DataFrame:
    """Load CSV and do basic validation. Returns cleaned DataFrame."""
    df = pd.read_csv(path_or_buffer)
    df.columns = [c.strip() for c in df.columns]

    # Drop fully empty rows
    df.dropna(how="all", inplace=True)

    # Coerce numeric columns
    for col in EXPENSE_COLS + ["Income", "Disposable_Income",
                                "Desired_Savings", "Desired_Savings_Percentage"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns used across the dashboard."""
    df = df.copy()

    present_expense_cols = [c for c in EXPENSE_COLS if c in df.columns]

    df["Total_Expenses"] = df[present_expense_cols].sum(axis=1)
    df["Savings_Rate_%"] = ((df["Income"] - df["Total_Expenses"]) /
                             df["Income"].replace(0, np.nan) * 100).round(1)
    df["Expense_to_Income_%"] = (df["Total_Expenses"] /
                                  df["Income"].replace(0, np.nan) * 100).round(1)

    # Savings gap: desired vs actual
    df["Actual_Savings"] = (df["Income"] - df["Total_Expenses"]).clip(lower=0)
    df["Savings_Gap"] = (df["Desired_Savings"] - df["Actual_Savings"]).round(2)

    # Total potential savings
    present_ps = [c for c in POTENTIAL_SAVINGS_COLS if c in df.columns]
    if present_ps:
        df["Total_Potential_Savings"] = df[present_ps].sum(axis=1).round(2)

    return df


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean spending per expense category across all individuals."""
    present = [c for c in EXPENSE_COLS if c in df.columns]
    means   = df[present].mean().round(2)
    return (pd.DataFrame({"Category": means.index, "Avg_Spend": means.values})
              .sort_values("Avg_Spend", ascending=False)
              .reset_index(drop=True))


def city_tier_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "City_Tier" not in df.columns:
        return pd.DataFrame()
    return (df.groupby("City_Tier")
              .agg(Avg_Income=("Income","mean"),
                   Avg_Expenses=("Total_Expenses","mean"),
                   Avg_Savings_Rate=("Savings_Rate_%","mean"),
                   Count=("Income","count"))
              .round(2)
              .reset_index())


def occupation_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "Occupation" not in df.columns:
        return pd.DataFrame()
    return (df.groupby("Occupation")
              .agg(Avg_Income=("Income","mean"),
                   Avg_Expenses=("Total_Expenses","mean"),
                   Count=("Income","count"))
              .round(2)
              .reset_index()
              .sort_values("Avg_Income", ascending=False))
