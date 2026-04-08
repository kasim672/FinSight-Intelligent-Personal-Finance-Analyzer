# 💹 FinSight — Intelligent Personal Finance Analyzer

> **Two-phase analytics pipeline:** Exploratory Data Analysis → Interactive Dashboard

---

## 🗂️ Project Structure

```
finsight/
│
├── analysis.ipynb          ← Phase 1: EDA in Jupyter
├── app.py                  ← Phase 2: Streamlit Dashboard
├── generate_data.py        ← Synthetic dataset generator
├── finance_data.csv        ← Sample dataset (500 rows, 27 cols)
├── requirements.txt
├── README.md
│
└── utils/
    ├── __init__.py
    ├── preprocessing.py    ← Load, clean, feature engineering
    ├── analytics.py        ← KPIs, insights, age-bucket stats
    └── visualizations.py   ← All Plotly chart factories
```

---

## 🚀 Quick Start

### 1 — Clone / unzip the project

```bash
cd finsight
```

### 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### 3 — (Optional) Generate a fresh synthetic dataset

```bash
python generate_data.py
```

### 4 — Run the Jupyter Notebook (EDA)

```bash
jupyter notebook analysis.ipynb
```

### 5 — Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📊 Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| `Income` | float | Monthly income (₹) |
| `Age` | int | Age of individual |
| `Dependents` | int | No. of financial dependants |
| `Occupation` | str | Salaried / Self-Employed / etc. |
| `City_Tier` | str | Tier 1 / 2 / 3 |
| `Rent` … `Miscellaneous` | float | 11 monthly expense categories (₹) |
| `Desired_Savings_Percentage` | float | Target savings % |
| `Desired_Savings` | float | Target savings amount (₹) |
| `Disposable_Income` | float | Income − all expenses |
| `Potential_Savings_*` | float | 8 potential-saving estimates |

The project also accepts any CSV that follows the same column names — upload directly via the dashboard sidebar.

---

## 🌐 Dashboard Features

| Tab | Contents |
|-----|----------|
| 🏠 **Overview** | KPI cards · Donut expense chart · City bar chart · Insights panel |
| 💳 **Spending** | Correlation heatmap · Potential savings bar · Category ranking table |
| 📈 **Savings & Goals** | Scatter plots · Savings gap metrics |
| 🌍 **Demographics** | Age-group dual-axis chart · Occupation bars · City tier table |
| 🗃️ **Raw Data** | Filtered table · CSV download |

**Sidebar filters:** City Tier · Occupation · Age range

---

## 🧠 Analytical Pipeline

```
generate_data.py
     │
     ▼
finance_data.csv
     │
     ├──► analysis.ipynb  (EDA: matplotlib / seaborn)
     │         • Load & validate
     │         • Feature engineering
     │         • 6 visualisation sections
     │         • Summary takeaways
     │
     └──► app.py  (Streamlit)
               └── utils/
                   ├── preprocessing.py
                   ├── analytics.py
                   └── visualizations.py (Plotly)
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Data wrangling | `pandas`, `numpy` |
| EDA visuals | `matplotlib`, `seaborn` |
| Dashboard charts | `plotly` |
| Web app | `streamlit` |
| Notebooks | `jupyter`, `nbformat` |

---

## 📌 Key Insights Generated

- Top expense category & % of income
- Savings shortfall / surplus vs desired goal
- Biggest cost-reduction opportunity
- Expense-to-income ratio alert
- Age vs savings pattern

---

*Built as a complete data analytics portfolio project.*
