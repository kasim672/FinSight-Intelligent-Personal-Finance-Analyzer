import pandas as pd
import numpy as np
from typing import Tuple, Dict, List


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data and perform initial validation"""
    df = pd.read_csv(filepath)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess financial data
    - Handle missing values
    - Ensure correct data types
    - Create derived columns
    """
    df = df.copy()
    
    # Fill missing values with 0 for expense columns
    expense_cols = ['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 
                    'Transport', 'Eating_Out', 'Entertainment', 'Utilities', 
                    'Healthcare', 'Education', 'Miscellaneous']
    
    for col in expense_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Ensure numeric columns are float
    numeric_cols = df.select_dtypes(include=['object']).columns
    for col in numeric_cols:
        if col not in ['Occupation', 'City_Tier']:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
    
    return df


def get_expense_categories() -> List[str]:
    """Return list of expense categories"""
    return ['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 
            'Transport', 'Eating_Out', 'Entertainment', 'Utilities', 
            'Healthcare', 'Education', 'Miscellaneous']


def calculate_total_expenses(df: pd.DataFrame) -> pd.Series:
    """Calculate total monthly expenses for each individual"""
    expense_cols = get_expense_categories()
    return df[expense_cols].sum(axis=1)


def get_category_summary(df: pd.DataFrame) -> Dict[str, float]:
    """Get total spending by category"""
    expense_cols = get_expense_categories()
    summary = {}
    for col in expense_cols:
        summary[col] = df[col].sum()
    return summary


def get_top_categories(df: pd.DataFrame, top_n: int = 5) -> Dict[str, float]:
    """Get top N spending categories"""
    summary = get_category_summary(df)
    sorted_summary = dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))
    return dict(list(sorted_summary.items())[:top_n])


def get_statistics(df: pd.DataFrame) -> Dict:
    """Calculate key financial statistics"""
    expense_cols = get_expense_categories()
    total_expenses = df[expense_cols].sum(axis=1)
    
    stats = {
        'total_income': df['Income'].sum(),
        'total_expenses': total_expenses.sum(),
        'avg_income': df['Income'].mean(),
        'avg_expenses': total_expenses.mean(),
        'total_disposable': df['Disposable_Income'].sum(),
        'avg_disposable': df['Disposable_Income'].mean(),
        'total_potential_savings': df[[col for col in df.columns if 'Potential_Savings' in col]].sum().sum(),
    }
    return stats


def get_occupation_summary(df: pd.DataFrame) -> Dict[str, float]:
    """Get average spending by occupation"""
    expense_cols = get_expense_categories()
    df['Total_Expenses'] = df[expense_cols].sum(axis=1)
    return df.groupby('Occupation')['Total_Expenses'].mean().to_dict()


def get_city_tier_summary(df: pd.DataFrame) -> Dict[str, float]:
    """Get average spending by city tier"""
    expense_cols = get_expense_categories()
    df['Total_Expenses'] = df[expense_cols].sum(axis=1)
    return df.groupby('City_Tier')['Total_Expenses'].mean().to_dict()


def get_age_group_summary(df: pd.DataFrame, bins: int = 5) -> Dict:
    """Get spending patterns by age groups"""
    expense_cols = get_expense_categories()
    df['Total_Expenses'] = df[expense_cols].sum(axis=1)
    df['Age_Group'] = pd.cut(df['Age'], bins=bins)
    return df.groupby('Age_Group')['Total_Expenses'].agg(['mean', 'count']).to_dict()


def get_savings_analysis(df: pd.DataFrame) -> Dict:
    """Analyze savings potential"""
    potential_cols = [col for col in df.columns if 'Potential_Savings' in col]
    
    analysis = {
        'total_potential_savings': df[potential_cols].sum().sum(),
        'avg_potential_savings': df[potential_cols].sum(axis=1).mean(),
        'by_category': df[potential_cols].sum().to_dict(),
    }
    return analysis


def filter_by_occupation(df: pd.DataFrame, occupation: str) -> pd.DataFrame:
    """Filter data by occupation"""
    if occupation == 'All':
        return df
    return df[df['Occupation'] == occupation]


def filter_by_city_tier(df: pd.DataFrame, city_tier: str) -> pd.DataFrame:
    """Filter data by city tier"""
    if city_tier == 'All':
        return df
    return df[df['City_Tier'] == city_tier]


def filter_by_age_range(df: pd.DataFrame, min_age: int, max_age: int) -> pd.DataFrame:
    """Filter data by age range"""
    return df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]
