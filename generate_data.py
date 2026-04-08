import argparse
import time
import numpy as np
import pandas as pd

# ── CLI ───────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Generate a synthetic Indian Personal Finance dataset.",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "rows",
    nargs="?",
    type=int,
    default=500,
    help="Number of rows to generate (default: 500)\nExamples: 1000, 5000, 20000",
)
parser.add_argument(
    "--seed",
    type=int,
    default=42,
    metavar="INT",
    help="Random seed for reproducibility (default: 42)",
)
parser.add_argument(
    "--out",
    type=str,
    default="finance_data.csv",
    metavar="FILE",
    help="Output CSV file name (default: finance_data.csv)",
)
args = parser.parse_args()

# ── Validate ──────────────────────────────────────────────────────────────────
if args.rows < 10:
    parser.error("rows must be at least 10.")
if args.rows > 1_000_000:
    parser.error("rows cannot exceed 1 000 000.")

# ── Generate ──────────────────────────────────────────────────────────────────
N = args.rows
np.random.seed(args.seed)

print(f"⚙️  Generating {N:,} rows  (seed={args.seed}) ...")
t0 = time.time()

OCCUPATIONS = ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Government Employee"]
CITY_TIERS  = ["Tier 1", "Tier 2", "Tier 3"]

def _clamp(arr, lo=0):
    return np.maximum(arr, lo).round(2)

age        = np.random.randint(22, 62, N)
dependents = np.random.choice([0, 1, 2, 3, 4], N, p=[0.25, 0.30, 0.25, 0.15, 0.05])
occupation = np.random.choice(OCCUPATIONS, N, p=[0.45, 0.20, 0.15, 0.12, 0.08])
city_tier  = np.random.choice(CITY_TIERS,  N, p=[0.40, 0.38, 0.22])

base_income = np.where(city_tier == "Tier 1", 75000,
              np.where(city_tier == "Tier 2", 50000, 35000))
income = _clamp(base_income + np.random.normal(0, 15000, N))

rent           = _clamp(income * np.random.uniform(0.15, 0.35, N))
loan_repayment = _clamp(income * np.random.uniform(0.00, 0.20, N))
insurance      = _clamp(income * np.random.uniform(0.01, 0.06, N))
groceries      = _clamp(income * np.random.uniform(0.05, 0.15, N))
transport      = _clamp(income * np.random.uniform(0.03, 0.10, N))
eating_out     = _clamp(income * np.random.uniform(0.02, 0.12, N))
entertainment  = _clamp(income * np.random.uniform(0.01, 0.08, N))
utilities      = _clamp(income * np.random.uniform(0.02, 0.07, N))
healthcare     = _clamp(income * np.random.uniform(0.01, 0.06, N))
education      = _clamp(income * np.random.uniform(0.00, 0.10, N) * (dependents > 0))
miscellaneous  = _clamp(income * np.random.uniform(0.01, 0.06, N))

total_expenses = (rent + loan_repayment + insurance + groceries + transport +
                  eating_out + entertainment + utilities + healthcare +
                  education + miscellaneous)

disposable_income   = _clamp(income - total_expenses)
desired_savings_pct = np.random.uniform(10, 35, N).round(1)
desired_savings     = (income * desired_savings_pct / 100).round(2)

ps = lambda cat: _clamp(cat * np.random.uniform(0.10, 0.30, N))

df = pd.DataFrame({
    "Income":                         income.round(2),
    "Age":                            age,
    "Dependents":                     dependents,
    "Occupation":                     occupation,
    "City_Tier":                      city_tier,
    "Rent":                           rent,
    "Loan_Repayment":                 loan_repayment,
    "Insurance":                      insurance,
    "Groceries":                      groceries,
    "Transport":                      transport,
    "Eating_Out":                     eating_out,
    "Entertainment":                  entertainment,
    "Utilities":                      utilities,
    "Healthcare":                     healthcare,
    "Education":                      education,
    "Miscellaneous":                  miscellaneous,
    "Desired_Savings_Percentage":     desired_savings_pct,
    "Desired_Savings":                desired_savings,
    "Disposable_Income":              disposable_income,
    "Potential_Savings_Groceries":    ps(groceries),
    "Potential_Savings_Transport":    ps(transport),
    "Potential_Savings_Eating_Out":   ps(eating_out),
    "Potential_Savings_Entertainment":ps(entertainment),
    "Potential_Savings_Utilities":    ps(utilities),
    "Potential_Savings_Healthcare":   ps(healthcare),
    "Potential_Savings_Education":    ps(education),
    "Potential_Savings_Miscellaneous":ps(miscellaneous),
})

df.to_csv(args.out, index=False)

elapsed = time.time() - t0
size_kb = df.memory_usage(deep=True).sum() / 1024

print(f"✅  {args.out} saved — {len(df):,} rows · {len(df.columns)} columns · {size_kb:,.0f} KB in memory · {elapsed:.2f}s")