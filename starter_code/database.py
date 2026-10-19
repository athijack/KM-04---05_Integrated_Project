"""
database.py
------------
Task 3: Build a relational database from your cleaned data.

This module covers KM-04 topics: Introduction to Databases (DBMS,
components, characteristics) and Structured Query Language (SQL).

We use Python's built-in sqlite3 module — no extra install needed.
SQLite stores the whole database in a single file (store.db), which
makes it easy to include as evidence.

Tables:
  products — product catalogue with prices and stock status
  sales    — individual sales transactions linked to products

SQL queries included:
  1. query_total_revenue_per_product  — JOIN + SUM (required)
  2. query_best_selling_product       — SUM + ORDER BY + LIMIT 1
  3. query_sales_by_payment_method    — COUNT + GROUP BY
  4. query_custom_one                 — Revenue per category (GROUP BY category)
  5. query_custom_two                 — Monthly revenue trend (GROUP BY month)
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    """
    Open (and create, if needed) the SQLite database file.

    Returns:
        an open sqlite3.Connection
    """
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create the `products` and `sales` tables if they don't already exist.

    Design:
      products
        - product_id   TEXT PRIMARY KEY
        - product_name TEXT NOT NULL
        - category     TEXT
        - unit_price   REAL
        - in_stock     TEXT

      sales
        - sale_id        TEXT PRIMARY KEY
        - product_id     TEXT, FOREIGN KEY references products(product_id)
        - quantity       INTEGER
        - sale_date      TEXT (stored as YYYY-MM-DD)
        - payment_method TEXT
        - customer_type  TEXT

    Primary keys enforce uniqueness (data integrity).
    The foreign key on sales.product_id enforces referential integrity —
    every sale must reference a product that actually exists.
    """
    # Enable foreign key enforcement (SQLite has it off by default)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id   TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category     TEXT,
            unit_price   REAL,
            in_stock     TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id        TEXT PRIMARY KEY,
            product_id     TEXT,
            quantity       INTEGER,
            sale_date      TEXT,
            payment_method TEXT,
            customer_type  TEXT,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """)

    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """
    Insert every row of the cleaned products DataFrame into the
    products table. Uses INSERT OR IGNORE so re-running main.py
    does not raise a duplicate key error.
    """
    # Clear existing rows first so re-runs stay idempotent
    conn.execute("DELETE FROM products")

    for row in products_df.itertuples(index=False):
        conn.execute(
            """
            INSERT OR IGNORE INTO products
                (product_id, product_name, category, unit_price, in_stock)
            VALUES (?, ?, ?, ?, ?)
            """,
            (row.product_id, row.product_name, row.category,
             row.unit_price, str(row.in_stock))
        )

    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """
    Insert every row of the cleaned sales DataFrame into the sales table.
    Uses INSERT OR IGNORE so re-running main.py does not raise errors.
    """
    # Clear existing rows first so re-runs stay idempotent
    conn.execute("DELETE FROM sales")

    for row in sales_df.itertuples(index=False):
        conn.execute(
            """
            INSERT OR IGNORE INTO sales
                (sale_id, product_id, quantity, sale_date,
                 payment_method, customer_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (row.sale_id, row.product_id, int(row.quantity),
             row.sale_date, row.payment_method, row.customer_type)
        )

    conn.commit()


# ---------------------------------------------------------------------
# SQL QUERIES
# ---------------------------------------------------------------------

def query_total_revenue_per_product(conn: sqlite3.Connection):
    """
    Query 1 (required): Total revenue per product.

    Business question: Which products are making Thabo the most money?

    Uses a JOIN between sales and products on product_id, multiplies
    quantity by unit_price for each sale, then SUMs per product.
    Returns (product_name, total_revenue) sorted highest first.
    """
    sql = """
        SELECT
            p.product_name,
            ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """
    Query 2 (required): Best-selling product by total units sold.

    Business question: Which single product has sold the most units overall?

    Uses SUM(quantity) grouped by product, ordered descending, limited to 1.
    Returns (product_name, total_units_sold).
    """
    sql = """
        SELECT
            p.product_name,
            SUM(s.quantity) AS total_units
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_units DESC
        LIMIT 1
    """
    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """
    Query 3 (required): Number of transactions per payment method.

    Business question: How are customers paying? Is Thabo's card machine
    getting enough use, or is most business still cash?

    Uses COUNT(*) grouped by payment_method.
    Returns (payment_method, transaction_count).
    """
    sql = """
        SELECT
            payment_method,
            COUNT(*) AS transaction_count
        FROM sales
        GROUP BY payment_method
        ORDER BY transaction_count DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """
    Query 4 (custom): Total revenue per product category.

    Business question: Which category brings in the most revenue?
    This helps Thabo decide where to focus his shelf space and stock.

    Uses a JOIN and SUM grouped by category.
    Returns (category, total_revenue) sorted highest first.
    """
    sql = """
        SELECT
            p.category,
            ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """
    Query 5 (custom): Monthly revenue trend.

    Business question: Is the store's revenue growing month on month?
    Thabo wants to see if January or February was a better trading month.

    Uses SUBSTR to extract YYYY-MM from sale_date, then SUMs revenue
    per month. Returns (month, total_revenue) sorted chronologically.
    """
    sql = """
        SELECT
            SUBSTR(s.sale_date, 1, 7) AS month,
            ROUND(SUM(s.quantity * p.unit_price), 2) AS monthly_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY month
        ORDER BY month ASC
    """
    return conn.execute(sql).fetchall()
