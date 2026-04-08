"""
FinSight: Intelligent Personal Finance Analyzer
Streamlit Dashboard Application - Light Theme
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

# Professional Light Theme CSS
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 40px 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .header-title {
        color: #FFFFFF;
        font-size: 2.8em;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1em;
        margin-top: 8px;
        font-weight: 300;
    }
    
    /* Card styling */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E8E8E8;
        padding: 24px;
        border-radius: 10px;
        margin: 12px 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: #4CAF50;
    }
    
    .insight-card {
        background-color: #F9F9F9;
        border-left: 4px solid #4CAF50;
        padding: 20px;
        border-radius: 8px;
        margin: 12px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .insight-card-success {
        border-left-color: #4CAF50;
        background-color: #F1F8F4;
    }
    
    .insight-card-warning {
        border-left-color: #FF9800;
        background-color: #FFF3E0;
    }
    
    .insight-card-info {
        border-left-color: #2196F3;
        background-color: #E3F2FD;
    }
    
    /* Section headers */
    .section-header {
        color: #222222;
        font-size: 1.6em;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #4CAF50;
    }
    
    .subsection-header {
        color: #333333;
        font-size: 1.2em;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #E0E0E0, transparent);
        margin: 30px 0;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        color: #4CAF50;
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    /* Text styling */
    .text-muted {
        color: #666666;
        font-size: 0.95em;
    }
    
    .text-success {
        color: #4CAF50;
        font-weight: 600;
    }
    
    .text-warning {
        color: #FF9800;
        font-weight: 600;
    }
    
    .text-info {
        color: #2196F3;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999999;
        font-size: 0.9em;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #E8E8E8;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2em;
        }
        .section-header {
            font-size: 1.3em;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header-container">
        <div class="header-title">💰 FinSight</div>
        <div class="header-subtitle">Intelligent Personal Finance Analyzer</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="color: #666666; font-size: 1.05em; margin-bottom: 20px;">
    Analyze spending patterns, identify savings opportunities, and make informed financial decisions.
    </p>
""", unsafe_allow_html=True)

# Sidebar - File upload and filters
st.sidebar.markdown('<div class="sidebar-header">📁 Data Upload</div>', unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is not None:
    # Load and preprocess data
    df = load_data(uploaded_file)
    df = preprocess_data(df)
    
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-header">🔍 Filter Options</div>', unsafe_allow_html=True)
    
    # Occupation filter
    occupations = ['All'] + sorted(df['Occupation'].unique().tolist())
    selected_occupation = st.sidebar.selectbox("Occupation", occupations, key="occ_filter")
    df_filtered = filter_by_occupation(df, selected_occupation)
    
    # City tier filter
    city_tiers = ['All'] + sorted(df_filtered['City_Tier'].unique().tolist())
    selected_city = st.sidebar.selectbox("City Tier", city_tiers, key="city_filter")
    df_filtered = filter_by_city_tier(df_filtered, selected_city)
    
    # Age range filter
    min_age, max_age = st.sidebar.slider(
        "Age Range",
        int(df['Age'].min()),
        int(df['Age'].max()),
        (int(df['Age'].min()), int(df['Age'].max())),
        key="age_filter"
    )
    df_filtered = filter_by_age_range(df_filtered, min_age, max_age)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
        <div style="background-color: #F1F8F4; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
            <p style="margin: 0; color: #222222; font-weight: 600;">📊 Records Shown</p>
            <p style="margin: 5px 0 0 0; color: #4CAF50; font-size: 1.3em; font-weight: 700;">{len(df_filtered):,} / {len(df):,}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content - Key Metrics
    st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
    
    stats = get_statistics(df_filtered)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Income",
            f"₹{stats['total_income']/1e7:.2f}Cr",
            delta=f"Avg: ₹{stats['avg_income']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Total Expenses",
            f"₹{stats['total_expenses']/1e7:.2f}Cr",
            delta=f"Avg: ₹{stats['avg_expenses']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Disposable Income",
            f"₹{stats['total_disposable']/1e7:.2f}Cr",
            delta=f"Avg: ₹{stats['avg_disposable']:,.0f}"
        )
    
    with col4:
        st.metric(
            "Potential Savings",
            f"₹{stats['total_potential_savings']/1e7:.2f}Cr",
            delta="Optimization opportunity"
        )
    
    # Visualizations - Spending Analysis
    st.markdown('<div class="section-header">📈 Spending Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Pie chart - Category-wise spending
    with col1:
        st.markdown('<div class="subsection-header">Category-wise Distribution</div>', unsafe_allow_html=True)
        category_summary = get_category_summary(df_filtered)
        fig_pie = px.pie(
            values=list(category_summary.values()),
            names=list(category_summary.keys()),
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#222222', size=11)
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Bar chart - Top categories
    with col2:
        st.markdown('<div class="subsection-header">Top 5 Spending Categories</div>', unsafe_allow_html=True)
        top_cats = get_top_categories(df_filtered, top_n=5)
        fig_bar = px.bar(
            x=list(top_cats.keys()),
            y=list(top_cats.values()),
            labels={'x': 'Category', 'y': 'Total Spending (₹)'},
            color=list(top_cats.values()),
            color_continuous_scale='Greens'
        )
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#222222', size=11),
            xaxis_tickangle=-45
        )
        fig_bar.update_traces(marker_line_color='#4CAF50', marker_line_width=1)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Income vs Expenses Analysis
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💵 Income vs Expenses Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subsection-header">Average Spending by Occupation</div>', unsafe_allow_html=True)
        occ_summary = get_occupation_summary(df_filtered)
        fig_occ = px.bar(
            x=list(occ_summary.keys()),
            y=list(occ_summary.values()),
            labels={'x': 'Occupation', 'y': 'Avg Spending (₹)'},
            color=list(occ_summary.values()),
            color_continuous_scale='Blues'
        )
        fig_occ.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#222222', size=11),
            xaxis_tickangle=-45
        )
        fig_occ.update_traces(marker_line_color='#2196F3', marker_line_width=1)
        st.plotly_chart(fig_occ, use_container_width=True)
    
    with col2:
        st.markdown('<div class="subsection-header">Average Spending by City Tier</div>', unsafe_allow_html=True)
        city_summary = get_city_tier_summary(df_filtered)
        fig_city = px.bar(
            x=list(city_summary.keys()),
            y=list(city_summary.values()),
            labels={'x': 'City Tier', 'y': 'Avg Spending (₹)'},
            color=list(city_summary.values()),
            color_continuous_scale='Purples'
        )
        fig_city.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#222222', size=11)
        )
        fig_city.update_traces(marker_line_color='#9C27B0', marker_line_width=1)
        st.plotly_chart(fig_city, use_container_width=True)
    
    # Savings Analysis
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 Savings Potential Analysis</div>', unsafe_allow_html=True)
    
    savings_analysis = get_savings_analysis(df_filtered)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div style="color: #4CAF50; font-size: 0.9em; font-weight: 600; margin-bottom: 8px;">💰 Total Potential Savings</div>
                <div style="color: #222222; font-size: 2em; font-weight: 700;">₹{:,.0f}</div>
                <div style="color: #666666; font-size: 0.9em; margin-top: 8px;">Avg per person: ₹{:,.0f}</div>
            </div>
        """.format(savings_analysis['total_potential_savings'], savings_analysis['avg_potential_savings']), 
        unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="subsection-header">Savings Opportunity by Category</div>', unsafe_allow_html=True)
        savings_by_cat = savings_analysis['by_category']
        clean_savings = {k.replace('Potential_Savings_', ''): v for k, v in savings_by_cat.items()}
        fig_savings = px.bar(
            x=list(clean_savings.keys()),
            y=list(clean_savings.values()),
            labels={'x': 'Category', 'y': 'Potential Savings (₹)'},
            color=list(clean_savings.values()),
            color_continuous_scale='Greens'
        )
        fig_savings.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#222222', size=10),
            xaxis_tickangle=-45,
            margin=dict(b=100)
        )
        fig_savings.update_traces(marker_line_color='#4CAF50', marker_line_width=1)
        st.plotly_chart(fig_savings, use_container_width=True)
    
    # Insights Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_summary = get_category_summary(df_filtered)
        highest_cat = max(category_summary, key=category_summary.get)
        highest_amount = category_summary[highest_cat]
        st.markdown(f"""
            <div class="insight-card insight-card-warning">
                <div style="font-size: 0.9em; color: #FF9800; font-weight: 600; margin-bottom: 8px;">⚠️ Highest Spending</div>
                <div style="font-size: 1.3em; color: #222222; font-weight: 700; margin-bottom: 4px;">{highest_cat}</div>
                <div style="font-size: 1.1em; color: #FF9800; font-weight: 600;">₹{highest_amount:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_expenses = df_filtered[get_expense_categories()].sum(axis=1).sum()
        total_income = df_filtered['Income'].sum()
        expense_ratio = (total_expenses / total_income * 100) if total_income > 0 else 0
        st.markdown(f"""
            <div class="insight-card insight-card-info">
                <div style="font-size: 0.9em; color: #2196F3; font-weight: 600; margin-bottom: 8px;">📊 Expense Ratio</div>
                <div style="font-size: 1.8em; color: #222222; font-weight: 700;">{expense_ratio:.1f}%</div>
                <div style="font-size: 0.9em; color: #666666; margin-top: 8px;">Of total income spent</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_savings = df_filtered['Disposable_Income'].mean()
        st.markdown(f"""
            <div class="insight-card insight-card-success">
                <div style="font-size: 0.9em; color: #4CAF50; font-weight: 600; margin-bottom: 8px;">✓ Avg Disposable Income</div>
                <div style="font-size: 1.3em; color: #222222; font-weight: 700;">₹{avg_savings:,.0f}</div>
                <div style="font-size: 0.9em; color: #666666; margin-top: 8px;">Per person monthly</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Detailed Statistics Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Detailed Category Breakdown</div>', unsafe_allow_html=True)
    
    category_summary = get_category_summary(df_filtered)
    summary_df = pd.DataFrame({
        'Category': list(category_summary.keys()),
        'Total Spending (₹)': [f"₹{v:,.0f}" for v in category_summary.values()],
        'Percentage': [f"{(v/sum(category_summary.values())*100):.1f}%" for v in category_summary.values()]
    })
    
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Data Preview
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if st.checkbox("📊 Show raw data", key="show_data"):
        st.markdown('<div class="subsection-header">Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.markdown("""
        <div style="background-color: #E3F2FD; border-left: 4px solid #2196F3; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <div style="color: #2196F3; font-size: 1.1em; font-weight: 600; margin-bottom: 10px;">👈 Get Started</div>
            <p style="color: #222222; margin: 8px 0;">Upload a CSV file in the sidebar to begin analyzing your financial data.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="margin-top: 30px;">
            <div class="subsection-header">How to Use FinSight</div>
            
            <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px; margin: 15px 0;">
                <div style="color: #4CAF50; font-weight: 600; margin-bottom: 8px;">1️⃣ Upload CSV</div>
                <p style="color: #666666; margin: 0;">Click the upload button in the sidebar to load your financial data</p>
            </div>
            
            <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px; margin: 15px 0;">
                <div style="color: #4CAF50; font-weight: 600; margin-bottom: 8px;">2️⃣ Apply Filters</div>
                <p style="color: #666666; margin: 0;">Use filter options to segment data by Occupation, City Tier, and Age Range</p>
            </div>
            
            <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px; margin: 15px 0;">
                <div style="color: #4CAF50; font-weight: 600; margin-bottom: 8px;">3️⃣ Analyze & Explore</div>
                <p style="color: #666666; margin: 0;">View interactive charts, metrics, and key insights about spending patterns</p>
            </div>
            
            <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px; margin: 15px 0;">
                <div style="color: #4CAF50; font-weight: 600; margin-bottom: 8px;">4️⃣ Identify Opportunities</div>
                <p style="color: #666666; margin: 0;">Get actionable insights and savings recommendations</p>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background-color: #F1F8F4; border-radius: 8px; border-left: 4px solid #4CAF50;">
            <div style="color: #4CAF50; font-weight: 600; margin-bottom: 10px;">📋 Expected CSV Columns</div>
            <p style="color: #666666; margin: 5px 0; font-size: 0.95em;">
                <strong>Demographics:</strong> Income, Age, Dependents, Occupation, City_Tier<br>
                <strong>Expenses:</strong> Rent, Loan_Repayment, Insurance, Groceries, Transport, Eating_Out, Entertainment, Utilities, Healthcare, Education, Miscellaneous<br>
                <strong>Financial:</strong> Disposable_Income, Desired_Savings_Percentage, Desired_Savings<br>
                <strong>Savings:</strong> Potential_Savings_* columns for each category
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>FinSight © 2024 | Intelligent Personal Finance Analyzer</p>
        <p style="font-size: 0.85em; margin-top: 8px;">Analyze • Optimize • Grow</p>
    </div>
""", unsafe_allow_html=True)
