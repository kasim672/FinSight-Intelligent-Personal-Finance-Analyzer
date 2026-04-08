"""
FinSight: Intelligent Personal Finance Analyzer
Streamlit Dashboard Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_data, preprocess_data, get_category_summary, get_top_categories,
    get_statistics, get_occupation_summary, get_city_tier_summary,
    get_savings_analysis, filter_by_occupation, filter_by_city_tier,
    filter_by_age_range, get_expense_categories
)

# Page configuration
st.set_page_config(
    page_title="FinSight - Personal Finance Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="header-title">💰 FinSight</div>', unsafe_allow_html=True)
st.markdown("### Intelligent Personal Finance Analyzer")
st.markdown("Analyze spending patterns, identify savings opportunities, and make informed financial decisions.")

# Sidebar - File upload and filters
st.sidebar.header("📁 Data Upload & Filters")

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is not None:
    # Load and preprocess data
    df = load_data(uploaded_file)
    df = preprocess_data(df)
    
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filter Options")
    
    # Occupation filter
    occupations = ['All'] + sorted(df['Occupation'].unique().tolist())
    selected_occupation = st.sidebar.selectbox("Select Occupation", occupations)
    df_filtered = filter_by_occupation(df, selected_occupation)
    
    # City tier filter
    city_tiers = ['All'] + sorted(df_filtered['City_Tier'].unique().tolist())
    selected_city = st.sidebar.selectbox("Select City Tier", city_tiers)
    df_filtered = filter_by_city_tier(df_filtered, selected_city)
    
    # Age range filter
    min_age, max_age = st.sidebar.slider(
        "Select Age Range",
        int(df['Age'].min()),
        int(df['Age'].max()),
        (int(df['Age'].min()), int(df['Age'].max()))
    )
    df_filtered = filter_by_age_range(df_filtered, min_age, max_age)
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Records shown: {len(df_filtered)} out of {len(df)}")
    
    # Main content
    # Key Metrics
    st.markdown("---")
    st.subheader("📊 Key Metrics")
    
    stats = get_statistics(df_filtered)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Income",
            f"₹{stats['total_income']:,.0f}",
            delta=f"Avg: ₹{stats['avg_income']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Total Expenses",
            f"₹{stats['total_expenses']:,.0f}",
            delta=f"Avg: ₹{stats['avg_expenses']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Disposable Income",
            f"₹{stats['total_disposable']:,.0f}",
            delta=f"Avg: ₹{stats['avg_disposable']:,.0f}"
        )
    
    with col4:
        st.metric(
            "Potential Savings",
            f"₹{stats['total_potential_savings']:,.0f}",
            delta="Optimization opportunity"
        )
    
    # Visualizations
    st.markdown("---")
    st.subheader("📈 Spending Analysis")
    
    col1, col2 = st.columns(2)
    
    # Pie chart - Category-wise spending
    with col1:
        st.markdown("#### Category-wise Spending Distribution")
        category_summary = get_category_summary(df_filtered)
        fig_pie = px.pie(
            values=list(category_summary.values()),
            names=list(category_summary.keys()),
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Bar chart - Top categories
    with col2:
        st.markdown("#### Top 5 Spending Categories")
        top_cats = get_top_categories(df_filtered, top_n=5)
        fig_bar = px.bar(
            x=list(top_cats.keys()),
            y=list(top_cats.values()),
            labels={'x': 'Category', 'y': 'Total Spending (₹)'},
            color=list(top_cats.values()),
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Income vs Expenses comparison
    st.markdown("---")
    st.subheader("💵 Income vs Expenses Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Occupation-wise spending
        st.markdown("#### Average Spending by Occupation")
        occ_summary = get_occupation_summary(df_filtered)
        fig_occ = px.bar(
            x=list(occ_summary.keys()),
            y=list(occ_summary.values()),
            labels={'x': 'Occupation', 'y': 'Avg Spending (₹)'},
            color=list(occ_summary.values()),
            color_continuous_scale='Viridis'
        )
        fig_occ.update_layout(height=400)
        st.plotly_chart(fig_occ, use_container_width=True)
    
    with col2:
        # City tier-wise spending
        st.markdown("#### Average Spending by City Tier")
        city_summary = get_city_tier_summary(df_filtered)
        fig_city = px.bar(
            x=list(city_summary.keys()),
            y=list(city_summary.values()),
            labels={'x': 'City Tier', 'y': 'Avg Spending (₹)'},
            color=list(city_summary.values()),
            color_continuous_scale='Plasma'
        )
        fig_city.update_layout(height=400)
        st.plotly_chart(fig_city, use_container_width=True)
    
    # Savings Analysis
    st.markdown("---")
    st.subheader("🎯 Savings Potential Analysis")
    
    savings_analysis = get_savings_analysis(df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Total Potential Savings",
            f"₹{savings_analysis['total_potential_savings']:,.0f}",
            delta=f"Avg per person: ₹{savings_analysis['avg_potential_savings']:,.0f}"
        )
    
    with col2:
        st.markdown("#### Savings Opportunity by Category")
        savings_by_cat = savings_analysis['by_category']
        # Clean up category names
        clean_savings = {k.replace('Potential_Savings_', ''): v for k, v in savings_by_cat.items()}
        fig_savings = px.bar(
            x=list(clean_savings.keys()),
            y=list(clean_savings.values()),
            labels={'x': 'Category', 'y': 'Potential Savings (₹)'},
            color=list(clean_savings.values()),
            color_continuous_scale='Greens'
        )
        fig_savings.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_savings, use_container_width=True)
    
    # Insights Section
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_summary = get_category_summary(df_filtered)
        highest_cat = max(category_summary, key=category_summary.get)
        highest_amount = category_summary[highest_cat]
        st.info(f"**Highest Spending Category:** {highest_cat}\n\n₹{highest_amount:,.0f}")
    
    with col2:
        total_expenses = df_filtered[get_expense_categories()].sum(axis=1).sum()
        total_income = df_filtered['Income'].sum()
        expense_ratio = (total_expenses / total_income * 100) if total_income > 0 else 0
        st.warning(f"**Expense Ratio:** {expense_ratio:.1f}%\n\nOf total income spent")
    
    with col3:
        avg_savings = df_filtered['Disposable_Income'].mean()
        st.success(f"**Avg Disposable Income:** ₹{avg_savings:,.0f}\n\nPer person monthly")
    
    # Detailed Statistics Table
    st.markdown("---")
    st.subheader("📋 Detailed Category Breakdown")
    
    category_summary = get_category_summary(df_filtered)
    summary_df = pd.DataFrame({
        'Category': list(category_summary.keys()),
        'Total Spending (₹)': [f"₹{v:,.0f}" for v in category_summary.values()],
        'Percentage': [f"{(v/sum(category_summary.values())*100):.1f}%" for v in category_summary.values()]
    })
    
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Data Preview
    st.markdown("---")
    st.subheader("📊 Data Preview")
    
    if st.checkbox("Show raw data"):
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("👈 Please upload a CSV file to get started!")
    st.markdown("""
    ### How to use FinSight:
    
    1. **Upload CSV**: Click the upload button in the sidebar to load your financial data
    2. **Apply Filters**: Use the filter options to segment your data by:
       - Occupation
       - City Tier
       - Age Range
    3. **Analyze**: View interactive charts and key metrics
    4. **Insights**: Get actionable insights about your spending patterns
    
    ### Expected CSV Columns:
    - Income, Age, Dependents, Occupation, City_Tier
    - Expense categories: Rent, Loan_Repayment, Insurance, Groceries, Transport, Eating_Out, Entertainment, Utilities, Healthcare, Education, Miscellaneous
    - Disposable_Income, Desired_Savings_Percentage, Desired_Savings
    - Potential_Savings_* columns for each category
    """)

st.markdown("---")
st.markdown("**FinSight** © 2024 | Intelligent Personal Finance Analyzer")
