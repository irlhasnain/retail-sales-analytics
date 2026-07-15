from database.db_connect import get_connection
import pandas as pd 

def monthly_revenue():
    conn = get_connection()
    query = """
    SELECT
        STRFTIME('%Y-%m', o.order_date) AS month,
        ROUND(SUM(oi.sales), 2) AS total_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY month
    ORDER BY month;
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

def top_product(limit=10):
    conn = get_connection()
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

def customer_segmentation():
    """RFM Analysis - Recency, Frequency, Monetary"""
    conn = get_connection()
    query = """
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(o.total_amount), 2) AS monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
    ORDER BY monetary DESC;
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result