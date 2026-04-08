# FinSight: Intelligent Personal Finance Analyzer

A comprehensive data analytics project that analyzes personal finance patterns and spending habits using exploratory data analysis and an interactive dashboard.

## 📋 Project Overview

FinSight follows a two-phase architecture:
- **Phase 1**: Jupyter Notebook for exploratory data analysis (EDA)
- **Phase 2**: Streamlit dashboard for interactive visualization and insights

## 📁 Project Structure

```
FinSight/
├── analysis.ipynb              # Jupyter Notebook for EDA
├── app.py                      # Streamlit dashboard application
├── utils.py                    # Utility functions for data processing
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── dataset/
    └── data.csv               # Indian personal finance dataset (20,000 records)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. Clone or navigate to the project directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📊 Phase 1: Jupyter Notebook Analysis

The `analysis.ipynb` notebook includes:
- Data loading and exploration
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Statistical summaries
- Visualizations using matplotlib and seaborn
- Key insights and findings

### Running the Notebook

```bash
jupyter notebook analysis.ipynb
```

## 🌐 Phase 2: Streamlit Dashboard

The `app.py` file creates an interactive web application with:
- CSV file upload capability
- Interactive filters (month, category, occupation)
- Real-time visualizations using Plotly
- Key metrics and insights
- Spending analysis and trends

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📈 Features

### Dashboard Capabilities
- **Upload CSV**: Load your own financial data
- **Interactive Filters**: Filter by month, category, and occupation
- **Visualizations**:
  - Pie chart: Category-wise spending distribution
  - Line chart: Monthly spending trends
  - Bar chart: Top spending categories
- **Insights Section**:
  - Highest spending category
  - Month with highest expense
  - Percentage changes and trends
  - Savings analysis

### Data Categories
- Rent
- Loan Repayment
- Insurance
- Groceries
- Transport
- Eating Out
- Entertainment
- Utilities
- Healthcare
- Education
- Miscellaneous

## 📊 Dataset Description

The dataset contains financial and demographic information for 20,000 individuals in India:
- **Income & Demographics**: Monthly income, age, dependents, occupation, city tier
- **Monthly Expenses**: 11 expense categories
- **Financial Goals**: Desired savings percentage and targets
- **Potential Savings**: Optimization opportunities across categories

## 🔧 Utility Functions

The `utils.py` module provides:
- Data loading and validation
- Data preprocessing and cleaning
- Category-wise aggregation
- Trend calculation
- Insight generation

## 💡 Key Insights Generated

- Total spending and disposable income analysis
- Category-wise spending distribution
- Monthly spending trends
- Highest and lowest spending months
- Savings potential identification
- Spending patterns by occupation and city tier

## 📝 Notes

- All monetary values are in INR (Indian Rupees)
- The dataset includes 20,000 individual records
- Analysis covers multiple demographic segments
- Potential savings are pre-calculated in the dataset

## 🎯 Use Cases

- Personal finance management
- Spending pattern analysis
- Budget optimization
- Financial planning
- Research on Indian spending habits

## 📄 License

This project is open source and available for educational and research purposes.
