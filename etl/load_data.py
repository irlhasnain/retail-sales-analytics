import pandas as pd 
import sys
sys.path.append("../database")  # Add the database directory to the system path
from database.db_connect import get_connection

def load_customer(df,conn):
    customer_df = df[['customer_id', 'customer_name', 'segment', 'region']].drop_duplicates()
    customer_df.to_sql('customer', conn, if_exists='replace', index=False)
    print(f"Loaded {len(customer)}customers")

def load_product(df,conn):
    product_df = df[['product_id', 'product_name', 'category', 'sub_category']].drop_duplicates()
    product_df.to_sql('product', conn, if_exists='replace', index=False)
    print(f"Loaded {len(product_df)} products")