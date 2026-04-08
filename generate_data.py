import numpy as np
import pandas as pd

np.random.seed(42)
N = 500  # rows (keep small so the repo stays lightweight)

OCCUPATIONS = ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Government Employee"]
CITY_TIERS   = ["Tier 1", "Tier 2", "Tier 3"]

def _clamp(arr, lo=0):
    return np.maximum(arr, lo).round(2)

age         = np.random.randint(22, 62, N)
dependents  = np.random.choice([0, 1, 2, 3, 4], N, p=[0.25, 0.30, 0.25, 0.15, 0.05])
occupation  = np.random.choice(OCCUPATIONS, N, p=[0.45, 0.20, 0.15, 0.12, 0.08])
city_tier   = np.random.choice(CITY_TIERS,  N, p=[0.40, 0.38, 0.22])

base_income = np.where(city_tier == "Tier 1", 75000,
              np.where(city_tier == "Tier 2", 50000, 35000))
income = _clamp(base_income + np.random.normal(0, 15000, N))

rent             = _clamp(income * np.random.uniform(0.15, 0.35, N))
loan_repayment   = _clamp(income * np.random.uniform(0.00, 0.20, N))
insurance        = _clamp(income * np.random.uniform(0.01, 0.06, N))
groceries        = _clamp(income * np.random.uniform(0.05, 0.15, N))
transport        = _clamp(income * np.random.uniform(0.03, 0.10, N))
eating_out       = _clamp(income * np.random.uniform(0.02, 0.12, N))
entertainment    = _clamp(income * np.random.uniform(0.01, 0.08, N))
utilities        = _clamp(income * np.random.uniform(0.02, 0.07, N))
healthcare       = _clamp(income * np.random.uniform(0.01, 0.06, N))
education        = _clamp(income * np.random.uniform(0.00, 0.10, N) * (dependents > 0))
miscellaneous    = _clamp(income * np.random.uniform(0.01, 0.06, N))

total_expenses = (rent + loan_repayment + insurance + groceries + transport +
                  eating_out + entertainment + utilities + healthcare +
                  education + miscellaneous)

disposable_income = _clamp(income - total_expenses)
desired_savings_pct = np.random.uniform(10, 35, N).round(1)
desired_savings = (income * desired_savings_pct / 100).round(2)

# Potential savings (10-30 % of each category)
ps = lambda cat: _clamp(cat * np.random.uniform(0.10, 0.30, N))

df = pd.DataFrame({
    "Income":                    income.round(2),
    "Age":                       age,
    "Dependents":                dependents,
    "Occupation":                occupation,
    "City_Tier":                 city_tier,
    "Rent":                      rent,
    "Loan_Repayment":            loan_repayment,
    "Insurance":                 insurance,
    "Groceries":                 groceries,
    "Transport":                 transport,
    "Eating_Out":                eating_out,
    "Entertainment":             entertainment,
    "Utilities":                 utilities,
    "Healthcare":                healthcare,
    "Education":                 education,
    "Miscellaneous":             miscellaneous,
    "Desired_Savings_Percentage":desired_savings_pct,
    "Desired_Savings":           desired_savings,
    "Disposable_Income":         disposable_income,
    "Potential_Savings_Groceries":     ps(groceries),
    "Potential_Savings_Transport":     ps(transport),
    "Potential_Savings_Eating_Out":    ps(eating_out),
    "Potential_Savings_Entertainment": ps(entertainment),
    "Potential_Savings_Utilities":     ps(utilities),
    "Potential_Savings_Healthcare":    ps(healthcare),
    "Potential_Savings_Education":     ps(education),
    "Potential_Savings_Miscellaneous": ps(miscellaneous),
})

df.to_csv("finance_data.csv", index=False)
print(f"✅  finance_data.csv created — {len(df)} rows, {len(df.columns)} columns")
