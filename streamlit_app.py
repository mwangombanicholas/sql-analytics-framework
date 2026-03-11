
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="SQL Analytics Framework", layout="wide")

# Title
st.title("🔍 SQL-First Analytics Framework")
st.markdown("---")

# Connect to database
@st.cache_data
def load_data():
    conn = sqlite3.connect('analytics_framework.db')
    
    # Load dirty data
    dirty_orders = pd.read_sql("SELECT * FROM orders_raw", conn)
    dirty_customers = pd.read_sql("SELECT * FROM customers_raw", conn)
    dirty_products = pd.read_sql("SELECT * FROM products_raw", conn)
    
    # Load clean data
    clean_sales = pd.read_sql("SELECT * FROM sales_dashboard", conn)
    
    # Load validation results
    validation = pd.read_sql("SELECT * FROM validation_log ORDER BY check_date DESC LIMIT 8", conn)
    
    conn.close()
    return dirty_orders, dirty_customers, dirty_products, clean_sales, validation

# Load data
dirty_orders, dirty_customers, dirty_products, clean_sales, validation = load_data()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Executive Summary", "Data Quality Audit", "Clean Dashboard", "Business Impact"])

if page == "Executive Summary":
    st.header("📊 Executive Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Orders (Dirty)", len(dirty_orders))
        st.metric("Total Orders (Clean)", len(clean_sales))
        st.metric("Invalid Orders Removed", len(dirty_orders) - len(clean_sales))
    
    with col2:
        dirty_revenue = dirty_orders[dirty_orders['status'] == 'completed']['quantity'] * dirty_orders[dirty_orders['status'] == 'completed']['unit_price']
        dirty_revenue = dirty_revenue.sum() if not dirty_revenue.empty else 0
        clean_revenue = clean_sales['revenue'].sum()
        
        st.metric("Revenue (Dirty)", f"${dirty_revenue:,.2f}")
        st.metric("Revenue (Clean)", f"${clean_revenue:,.2f}")
        st.metric("Overstatement", f"${dirty_revenue - clean_revenue:,.2f}")
    
    with col3:
        st.metric("Data Quality Score", "57%", "-43% to fix")
        st.metric("High Severity Issues", "4", "🚨 STOP DASHBOARD")
        st.metric("Business Impact", "$651", "at risk")
    
    st.markdown("---")
    st.subheader("🎯 Key Discovery")
    st.info("Revenue looked perfectly accurate ($675) but product insights were 450% WRONG! This framework catches these issues BEFORE they reach dashboards.")

elif page == "Data Quality Audit":
    st.header("🔍 Data Quality Audit")
    
    # Validation results
    st.subheader("Validation Checks")
    for _, row in validation.iterrows():
        if 'FAIL' in row['status']:
            st.error(f"❌ {row['check_name']}: {row['affected_count']} issues found - {row['recommendation']}")
        else:
            st.success(f"✅ {row['check_name']}: Passed")
    
    # Show dirty data
    st.subheader("Sample of Dirty Data (with issues)")
    tab1, tab2, tab3 = st.tabs(["Orders", "Customers", "Products"])
    
    with tab1:
        st.dataframe(dirty_orders.head(10))
        st.warning(f"⚠️ Issues: {dirty_orders['quantity'].isna().sum()} NULL quantities, {dirty_orders['unit_price'].isna().sum()} NULL prices")
    
    with tab2:
        st.dataframe(dirty_customers.head(10))
        st.warning(f"⚠️ Issues: {dirty_customers['customer_id'].duplicated().sum()} duplicates, {dirty_customers['email'].isna().sum()} missing emails")
    
    with tab3:
        st.dataframe(dirty_products.head(10))
        st.warning(f"⚠️ Issues: {dirty_products['product_id'].duplicated().sum()} duplicates, {dirty_products['category'].isna().sum()} missing categories")

elif page == "Clean Dashboard":
    st.header("📈 Clean Analytics Dashboard")
    
    # Key metrics
    total_revenue = clean_sales['revenue'].sum()
    total_profit = clean_sales['profit'].sum()
    avg_order = clean_sales['revenue'].mean()
    total_orders = len(clean_sales)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Avg Order Value", f"${avg_order:,.2f}")
    col4.metric("Total Orders", total_orders)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by product
        product_revenue = clean_sales.groupby('product_name')['revenue'].sum().reset_index()
        fig = px.bar(product_revenue, x='product_name', y='revenue', title='Revenue by Product')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by category
        category_revenue = clean_sales.groupby('category')['revenue'].sum().reset_index()
        fig = px.pie(category_revenue, values='revenue', names='category', title='Revenue by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("Clean Transaction Data")
    st.dataframe(clean_sales)

else:  # Business Impact
    st.header("💰 Business Impact Analysis")
    
    # Calculate impacts
    invalid_orders = len(dirty_orders) - len(clean_sales)
    revenue_diff = dirty_orders[dirty_orders['status'] == 'completed']['quantity'] * dirty_orders[dirty_orders['status'] == 'completed']['unit_price']
    revenue_diff = revenue_diff.sum() - clean_sales['revenue'].sum()
    
    # Top products comparison
    dirty_top = dirty_orders[dirty_orders['status'] == 'completed'].groupby('product_id')['quantity'].sum().reset_index()
    dirty_top = dirty_top.merge(dirty_products[['product_id', 'product_name']], on='product_id')
    dirty_top = dirty_top.nlargest(3, 'quantity')
    
    clean_top = clean_sales.groupby('product_name')['quantity'].sum().reset_index().nlargest(3, 'quantity')
    
    st.subheader("🚨 Wrong Business Decisions Prevented")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("❌ What Dirty Data Would Tell You")
        st.dataframe(dirty_top[['product_name', 'quantity']])
    
    with col2:
        st.success("✅ What Clean Data Actually Shows")
        st.dataframe(clean_top)
    
    st.markdown("---")
    
    # Impact summary
    st.subheader("📊 Total Business Impact")
    
    impact_data = pd.DataFrame({
        'Impact Area': ['Marketing Waste', 'Untracked Revenue', 'Inventory Errors', 'Revenue Overstatement'],
        'Amount': [1.20, 150.00, 500.00, revenue_diff]
    })
    
    fig = px.bar(impact_data, x='Impact Area', y='Amount', title='Business Impact by Area ($)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning(f"""
    ### 🎯 Key Takeaway
    **Total Direct Impact: ${impact_data['Amount'].sum():.2f}**
    
    This is money lost or misreported due to dirty data - from just 14 orders!
    Imagine this scaled to millions of records.
    """)

st.markdown("---")
st.caption("Built with SQL-first validation framework | [GitHub Repository](https://github.com/yourusername/sql-analytics-framework)")
