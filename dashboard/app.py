import streamlit as st
import sys
sys.path.append('.')
import pandas as pd
from database.db_connect import get_connection
from sql_queries.analytics import monthly_revenue, top_product, customer_segmentation

st.set_page_config(page_title="Retail Sales Anlytics",layout="wide")

st.title("📊 Retail Sales Analytics Dashboard")
st.write("Welcome to the dashboard!")
