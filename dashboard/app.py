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
st.line_chart(revenue_df.set_index('month')['total_revenue'])

st.subheader("🏆 Top 10 Products")
products_df = top_product(limit=10)
st.bar_chart(producsts_df.set_index('product_name')['total_sales'])

st.sidebar.header("Filters")

conn = get_connection()
regions = pd.read_sql_query("SELECT DISTINCT region FROM customers",conn)['region']
conn.close()

selected_region = st.sidebar.selectbox("Select Region",["All"]+regions)
