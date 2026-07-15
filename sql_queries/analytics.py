from database.db_connect import get_db_connection
import pandas as pd 

def monthly_revenue():
    conn = get_db_connection()
    query = """
    SELECT
        STRFTIME('%Y-%m', order_date) AS month,
        ROUND(SUM(total_amount), 2) AS total_revenue
    FROM orders
    GROUP BY month
    ORDER BY month;
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

def top_product(limit=10):
    conn = get_db_connection()
    query = f"""
    SELECT
        p.product_name,
        p.category,
        SUM(oi.sales) AS total_sales,
        SUM(oi.quantity) AS total_quantity_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id
    ORDER BY total_quantity_sold DESC
    LIMIT {limit};
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result