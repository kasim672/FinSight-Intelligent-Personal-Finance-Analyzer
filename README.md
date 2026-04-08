# FinSight — Intelligent Personal Finance Analyzer

> **Two-phase analytics pipeline:** Exploratory Data Analysis → Interactive Light-Theme Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=flat-square&logo=pandas&logoColor=white)

---

## 🗂️ Project Structure

```
finsight/
│
├── app.py                  ← Streamlit Dashboard (Light Theme)
├── analysis.ipynb          ← Jupyter EDA Notebook
├── generate_data.py        ← Synthetic dataset generator
├── finance_data.csv        ← Sample dataset (500 rows, 27 cols)
├── requirements.txt        ← Python dependencies
├── README.md               ← You are here
│
└── utils/
    ├── __init__.py
    ├── preprocessing.py    ← Load, validate, clean, feature engineering
    ├── analytics.py        ← KPIs, insights, age-bucket stats
    └── visualizations.py   ← Plotly light-theme chart factories
```

---

## ⚙️ Environment Setup

> **Recommended:** Use a virtual environment to keep dependencies isolated.

### Option A — `venv` (built-in, no extras needed)

```bash
# 1. Navigate to the project folder
cd finsight

# 2. Create a virtual environment named .venv
python -m venv .venv

# 3. Activate it
#    macOS / Linux:
source .venv/bin/activate
#    Windows (Command Prompt):
.venv\Scripts\activate.bat
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 4. Confirm you're in the venv (should show .venv path)
which python           # macOS/Linux
where python           # Windows

# 5. Install dependencies
pip install -r requirements.txt

# 6. To deactivate later:
deactivate
```

### Option B — `conda`

```bash
# 1. Create a new conda environment
conda create -n finsight python=3.11 -y

# 2. Activate it
conda activate finsight

# 3. Install dependencies
pip install -r requirements.txt
```

### Python Version

FinSight requires **Python 3.9 or higher**. Check your version with:

```bash
python --version
```

---

## 🚀 Running the Project

### Step 1 — Generate the sample dataset *(first-time only)*

```bash
python generate_data.py
# Output: finance_data.csv (500 rows, 27 columns)
```

---

## 📊 FinSight – Dataset Generator

Generates a realistic synthetic dataset mimicking the "Indian Personal Finance and Spending Habits" structure.

### Usage

```bash
python generate_data.py                  # default 500 rows
python generate_data.py 5000             # 5,000 rows
python generate_data.py 20000            # 20,000 rows (full Kaggle size)
python generate_data.py 10000 --seed 99  # custom random seed
python generate_data.py 1000 --out my_data.csv   # custom output file name
python generate_data.py --help           # show all options
```

---

### Step 2 — Exploratory Analysis (Jupyter Notebook)

```bash
jupyter notebook analysis.ipynb
```

The notebook walks through 9 sections:
1. Setup & Imports
2. Load & Inspect Data
3. Cleaning & Feature Engineering
4. Category-Wise Spending
5. Income Distribution by Tier & Occupation
6. Savings Rate Analysis
7. Age Group Breakdown
8. Correlation Heatmap
9. Summary & Key Takeaways

### Step 3 — Launch the Interactive Dashboard

```bash
streamlit run app.py
```

Then open **[http://localhost:8501](http://localhost:8501)** in your browser.

To stop the server: press `Ctrl + C` in the terminal.

---

## 🌐 Dashboard Overview

| Tab | What You'll Find |
|-----|-----------------|
| 🏠 **Overview** | 6 KPI cards · Donut expense chart · Auto-generated insights · City tier comparison · Savings distribution |
| 💳 **Spending** | Correlation heatmap · Potential savings bar · Medal-ranked category table |
| 📈 **Savings & Goals** | Savings gap KPIs · Income vs savings rate scatter by City Tier and Occupation |
| 🌍 **Demographics** | Age-group dual-axis chart · Occupation bars · City tier cards with progress bars |
| 🗃️ **Raw Data** | Filtered table with record count · CSV download button |

**Sidebar filters** drive all 5 tabs simultaneously:
- 🏙️ City Tier (Tier 1 / 2 / 3)
- 💼 Occupation (Salaried, Self-Employed, etc.)
- 🎂 Age Range (slider)

**Upload your own CSV** via the sidebar — any file matching the 27-column schema works.

---

## 📊 Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| `Income` | float | Monthly income (₹) |
| `Age` | int | Age of individual |
| `Dependents` | int | Number of dependants |
| `Occupation` | str | Salaried / Self-Employed / etc. |
| `City_Tier` | str | Tier 1 / 2 / 3 |
| `Rent` | float | Monthly rent (₹) |
| `Loan_Repayment` | float | Monthly loan repayments (₹) |
| `Insurance` | float | Insurance premium (₹) |
| `Groceries` | float | Grocery spending (₹) |
| `Transport` | float | Transport costs (₹) |
| `Eating_Out` | float | Restaurant / takeaway spending (₹) |
| `Entertainment` | float | Entertainment spending (₹) |
| `Utilities` | float | Utility bills (₹) |
| `Healthcare` | float | Healthcare costs (₹) |
| `Education` | float | Education spending (₹) |
| `Miscellaneous` | float | Other expenses (₹) |
| `Desired_Savings_Percentage` | float | Target savings % of income |
| `Desired_Savings` | float | Target savings amount (₹) |
| `Disposable_Income` | float | Income after all expenses (₹) |
| `Potential_Savings_*` | float | 8 estimated saving opportunities (₹) |

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Data Wrangling | `pandas`, `numpy` |
| EDA Visualizations | `matplotlib`, `seaborn` |
| Dashboard Charts | `plotly` (light theme) |
| Web App | `streamlit` |
| Notebooks | `jupyter`, `nbformat` |

---

## 🧠 Analytics Pipeline

```
generate_data.py
      │
      ▼
finance_data.csv
      │
      ├──► analysis.ipynb  ──── EDA (matplotlib / seaborn)
      │         • Load & validate
      │         • Feature engineering
      │         • 7 visualisation sections
      │         • Printed summary
      │
      └──► app.py  ──────────── Streamlit Dashboard
                └── utils/
                    ├── preprocessing.py  (clean + engineer)
                    ├── analytics.py      (KPIs + insights)
                    └── visualizations.py (8 Plotly charts)
```

---

## 💡 Auto-Generated Insights

The dashboard surfaces 5 dynamic insights from the filtered dataset:

1. 🏆 **Top Expense Category** — highest average spend + % of income
2. ⚠️ / ✅ **Savings Shortfall / Surplus** — vs desired savings goal
3. 💡 **Biggest Saving Opportunity** — which category has most potential
4. 📊 **Expense-to-Income Ratio** — alerts when > 75%
5. 📈 **Age vs Savings Pattern** — under-35 vs 35+ comparison

---

*Built as a complete data analytics portfolio project.*
*Covers: data cleaning · feature engineering · EDA · interactive dashboards · insight generation.*
