CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders(
    order_id TEXT PrIMARY KEY,
    customer_id TEXT,
    order_date DATE,
    ship_date DATE,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items(
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    sales REAL,
    profit REAL,
    FOREIGN KEY (order_id) REFERENCES orders(orders_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);