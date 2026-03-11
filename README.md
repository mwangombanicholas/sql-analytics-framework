# 🔍 SQL-First Analytics Framework

## 🎯 The Problem
Most dashboards look great but hide dirty data. I discovered that **revenue can look perfectly accurate while product insights are 450% WRONG!**

## 💡 The Solution
A SQL validation framework that catches data issues BEFORE they reach dashboards.

## 📊 Key Findings
- **$100 revenue overstatement** from dirty data
- **16 extra units** of wrong product would be ordered
- **57.1% data quality score** → Now 100% clean
- **$651 total business impact** from just 14 orders

## 🛠️ Technologies Used
- **SQL** (CTEs, Window Functions, Views, Validation Queries)
- **Python** (Pandas, Plotly, Streamlit)
- **SQLite** for database
- **Streamlit** for interactive dashboard

## 🚀 Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 📁 Project Structure
```
├── streamlit_app.py          # Main dashboard application
├── analytics_framework.db     # SQLite database with dirty & clean data
├── requirements.txt           # Python dependencies
├── data_quality_dashboard.html # Interactive quality dashboard
├── final_comparison_dashboard.html # Dirty vs clean comparison
└── README.md                  # This file
```

## 🔍 Key SQL Concepts Demonstrated

### 1. Data Quality Validation
```sql
-- Automated validation checks
SELECT 
    COUNT(*) - COUNT(DISTINCT customer_id) as duplicate_customers,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) as missing_emails
FROM customers_raw;
```

### 2. Deduplication with Window Functions
```sql
WITH deduped_customers AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY customer_name
        ) as rn
    FROM customers_raw
)
SELECT * FROM deduped_customers WHERE rn = 1;
```

### 3. Business Logic Implementation
```sql
CREATE VIEW sales_dashboard AS
SELECT 
    o.*,
    c.customer_name,
    p.product_name,
    o.revenue - (p.cost * o.quantity) as profit
FROM clean_orders o
JOIN clean_customers c ON o.customer_id = c.customer_id
JOIN clean_products p ON o.product_id = p.product_id;
```

## 📈 Business Impact
This framework prevents:
- ❌ Wrong marketing campaigns
- ❌ Incorrect inventory orders
- ❌ Inflated sales targets
- ❌ Bad business decisions

## 🎯 Key Insight
> "Revenue can look perfectly accurate while product insights are 450% wrong. Always validate at the most granular level!"

## 🚦 How to Run Locally
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run streamlit_app.py`

## 📬 Contact
[Your Name] - [Your LinkedIn] - [Your Email]

---
⭐ Star this repo if you found it useful!
