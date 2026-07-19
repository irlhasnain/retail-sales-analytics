import streamlit as st
import sys
sys.path.append('.')
import pandas as pd
from database.db_connect import get_connection
from sql_queries.analytics import monthly_revenue, top_product, customer_segmentation

st.set_page_config(page_title="Retail Sales Anlytics",layout="wide")

st.title("📊 Retail Sales Analytics Dashboard")
st.write("Welcome to the dashboard!")


conn = get_connection()

total_revenue = pd.read_sql_query("SELECT SUM(sales) as total FROM  order_items",conn)['total'][0]
total_order = pd.read_sql_query("SELECT COUNT(DISTINCT order_id) as total FROM orders",conn)['total'][0]
total_customer = pd.read_sql_query("SELECT COUNT(DISTINCT customer_id) as total FROM customers",conn)['total'][0]

conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue",f"${total_revenue:,.0f}")
col2.metric("Total_order",f"${total_order:,.0f}")
col3.metric("Total Customer",f"${total_customer:,.0f}")

st.subheader("📈 Monthly Revenue Trends")
revenue_df = monthly_revenue()
revenue_df['month'] = pd.to_datetime(revenue_df['month'])

min_date = revenue_df['month'].min().to_pydatetime()
max_date = revenue_df['month'].max().to_pydatetime()

date_range = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM"
)

# Filter karo selected range ke hisab se
filtered_revenue = revenue_df[
    (revenue_df['month'] >= date_range[0]) & (revenue_df['month'] <= date_range[1])
]

st.line_chart(filtered_revenue.set_index('month')['total_revenue'])

st.subheader("🏆 Top 10 Products")
products_df = top_product(limit=10)
st.bar_chart(products_df.set_index('product_name')['total_sales'])

st.sidebar.header("Filters")

conn = get_connection()
regions = pd.read_sql_query("SELECT DISTINCT region FROM customers",conn)['region'].tolist()
conn.close()

selected_region = st.sidebar.selectbox("Select Region",["All"]+regions)

conn = get_connection()

if selected_region == "All":
    query = """
    SELECT p.category, SUM(oi.sales) as total_sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category
    """
else:
    query = f"""
    SELECT p.category, SUM(oi.sales) as total_sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.region = '{selected_region}'
    GROUP BY p.category
    """

category_df = pd.read_sql_query(query, conn)
conn.close()

st.subheader(f"📦 Category Sales - {selected_region}")
st.bar_chart(category_df.set_index('category')['total_sales'])

import pickle

st.subheader("Revenue Forecast")

with open('models/forecast_model.pkl','rb') as f:
    model = pickle.load(f)

future = model.make_future_dataframe(periods = 6, freq = "ME")
forecast = model.predict(future)

st.line_chart(forecast.set_index('ds')[['yhat']])